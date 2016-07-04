# coding=utf-8

# ${PROJECTNAME}
# (c) Chris von Csefalvay, 2015.

"""
test_liveProcess is responsible for [brief description here].
"""
from unittest import TestCase
from processpathway import LiveProcess
import cv2

def imaging_process_identity(frame):
    return frame

def imaging_process_thresholding(frame):
        _, _frame = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)
        return frame

def imaging_process_convert_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def imaging_process_reconvert_to_BGR(frame):
     = cv2.cvtColor(, cv2.COLOR_)

    def reconvert_to_bgr(_frame):
        _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2BGR)
        return _frame


class TestLiveProcess(TestCase):
    def setUp(self):
        liveprocess = LiveProcess()

    def test_bind_process(self):
        self.fail()

    def test_start(self):
        self.fail()

    def test_stop(self):
        self.fail()

    def test_read(self):
        self.fail()

    def test_initialise_capture_device(self):
        self.fail()

    def test_screenshot(self):
        self.fail()

    def test_loop(self):
        self.fail()
