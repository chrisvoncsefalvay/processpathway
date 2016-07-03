# coding=utf-8

# 
# (c) Chris von Csefalvay, 2016.
#

"""
processpathway is a simple image processing framework for live computer vision applications supporting primarily one
functionality: displaying a live transformation (or several) of a video camera (webcam) input.

The model of processpathway is a four-step process:
1) Create pathway, provide it with pathway-level resources.
2) Give it a list of tasks to do, ordered neatly.
3) Bind the tasks in.
4) Run the loop and enjoy the show.

"""

import collections
import cv2
import time
import datetime
from imutils.video import WebcamVideoStream
import logging
import sys


class FPS:
    def __init__(self):
        """
        Initialises an FPS counter.
        """
        self.last_frame = datetime.datetime.now()
        self.fps = None

    def update(self):
        """
        Updates FPS counter. Call this every time you process a frame.
        :return: fps
        :rtype: float
        """
        self.fps = 1 / (datetime.datetime.now() - self.last_frame).total_seconds()
        self.last_frame = datetime.datetime.now()
        return self.fps

    def fps(self):
        """
        FPS getter.
        :return: fps
        :rtype: float
        """
        return self.fps

    def imprint_fps(self,
                    image_matrix_object,
                    font_face=cv2.FONT_HERSHEY_PLAIN,
                    font_scale=1,
                    color=(255, 32, 32),
                    thickness=1,
                    origin=(50, 50)):
        """
        Imprints the frame rate on the image in the pipeline.

        :param image_matrix_object: image matrix object in the pipeline
        :type image_matrix_object:
        :param font_face:
        :type font_face:
        :param font_scale:
        :type font_scale:
        :param color:
        :type color:
        :param thickness:
        :type thickness:
        :param origin:
        :type origin:
        :return:
        :rtype:
        """

        cv2.putText(img=image_matrix_object,
                    text="{framerate:.2f} FPS".format(framerate=self.fps),
                    org=origin,
                    fontFace=font_face,
                    fontScale=font_scale,
                    color=color,
                    thickness=thickness)

        return image_matrix_object


class LiveProcess:
    def __init__(self,
                 process=None,
                 logger=None,
                 application_name="liveprocess",
                 ch_log_level=logging.DEBUG,
                 fh_log_level=logging.DEBUG,
                 warmup=1.0,
                 source_device_id=0,
                 screencap=False,
                 fps=True):
        """
        Initialises a LiveProcessor that pipes a webcam image through a processing function and displays it.

        :param process: processing function to pipe the incoming image through
        :type process: function
        :param logger: logger to use for logging outgoing messages
        :type logger: logging.Logger
        :param application_name: application function (and window) name
        :type application_name: str
        :param ch_log_level: stream handler log level
        :type ch_log_level: int
        :param fh_log_level: file handler log level
        :type fh_log_level: int
        :param warmup: camera warmup time
        :type warmup: float
        :param source_device_id: identifier of source device
        :type source_device_id: int
        :param screencap: switch to enable/disable screencap capability
        :type screencap: bool
        :param fps: whether to show FPS
        :type fps: bool
        """
        self.vs = None
        self.process = process or collections.OrderedDict()
        self.warmup = warmup
        self.screencap = screencap
        self.application_name = application_name
        self.source_device_id = source_device_id
        self.fps = fps
        self.lastframetime = datetime.datetime.now()
        self.frame = None

        if self.fps:
            self.fps_counter = FPS()

        if not hasattr(self, "logger") or self.logger is None:
            logger = logging.getLogger(self.application_name)
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler(u"{application_name:s}.log".format(application_name=self.application_name))
            ch = logging.StreamHandler()
            fh.setLevel(fh_log_level)
            ch.setLevel(ch_log_level)
            formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s")
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            logger.addHandler(fh)
            logger.addHandler(ch)
            self.logger = logger

    def bind_process(self, process, bind_id=None):
        self.logger.debug(u"Binding process {process:s} to processing pathway.".format(process=process))
        if bind_id:
            if bind_id in self.process.keys():
                self.logger.warning("Insertion is overwriting function at position %d..." % bind_id)
            self.process[bind_id] = process
            self.logger.debug(
                "Bound function {func_name:s} into the processing queue at position {func_position:d}."
                    .format(func_name=process.func_name, func_position=bind_id))
        else:
            if len(self.process.keys()) is 0:
                bind_id =1
            else:
                bind_id = max(self.process.keys()) + 1
            self.process[bind_id] = process
            self.logger.debug(
                "Bound function {func_name:s} into the processing queue at position {func_position:d}."
                .format(func_name=process.func_name, func_position=bind_id))

    def start(self):
        return self.vs.start()

    def stop(self):
        return self.vs.stop()

    def read(self):
        return self.vs.read()

    def initialise_capture_device(self, capture_device_id=0):
        try:
            self.vs = WebcamVideoStream(src=self.source_device_id).start()
        except Exception as e:
            self.logger.error("Failed to initialise capture device: %s" % e.message)
            sys.exit(3)

    def loop(self):
        if not self.vs:
            self.logger.error(u"You cannot call the loop sequence before initialising the capture device!")
            sys.exit(4)
        elif not self.process:
            self.logger.error(u"You cannot call the loop sequence before binding a processing function!")
        else:
            if self.warmup > 0:
                self.logger.debug(
                    "Beginning sensor warmup sequence of {warmup:.2f} second(s).".format(warmup=self.warmup))
                time.sleep(self.warmup)
                self.logger.debug("Sensor warmup sequence finished. Beginning video feed-forward.")

            while self.vs:
                self.frame = self.read()
                for i in self.process:
                    self.frame = self.process[i](self.frame)

                if self.fps:
                    self.fps_counter.update()
                    self.fps_counter.imprint_fps(self.frame)

                cv2.imshow("%s - output 1" % self.application_name, self.frame)

                k = cv2.waitKey(30) & 0xFF
                if k == 27:
                    self.logger.debug("User close signal detected: closing application.")
                    self.logger.debug("Closing video feed.")
                    self.stop()
                    self.logger.debug("Video feed closed.")
                    self.logger.debug("Closing windows.")
                    cv2.destroyAllWindows()
                    self.logger.debug("Windows closed. Terminating application.")
                    break

            sys.exit(0)
