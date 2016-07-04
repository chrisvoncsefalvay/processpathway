# coding=utf-8

# ${PROJECTNAME}
# (c) Chris von Csefalvay, 2015.

"""
test_liveProcess is responsible for [brief description here].
"""
from collections import OrderedDict
from unittest import TestCase

import cv2

from processpathway import LiveProcess


def imaging_process_identity(frame):
    return frame

def imaging_process_thresholding(frame):
        _, _frame = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)
        return frame

def imaging_process_convert_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def imaging_process_reconvert_to_BGR(frame):
    return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)


def reconvert_to_bgr(frame):
    _frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    return frame


class TestLiveProcess(TestCase):
    def setUp(self):
        self.processor = LiveProcess(fps=True)

    def test_bind_single_process(self):
        self.processor.bind_process(imaging_process_thresholding)
        i = OrderedDict()
        i[1] = imaging_process_thresholding
        assert i == self.processor.process

    def test_bind_multiple_processes(self):
        self.processor.bind_process(imaging_process_identity, imaging_process_convert_to_grayscale)
        i = OrderedDict()
        i[1] = imaging_process_identity
        i[2] = imaging_process_convert_to_grayscale
        assert i == self.processor.process

    def test_bind_ordered_processes(self):
        self.processor.bind_process(imaging_process_identity, bind_id=2)
        self.processor.bind_process(imaging_process_thresholding, bind_id=1)
        i = OrderedDict()
        i[2] = imaging_process_identity
        i[1] = imaging_process_thresholding
        assert i == self.processor.process
