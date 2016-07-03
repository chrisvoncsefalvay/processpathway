# coding=utf-8

# 
# (c) Chris von Csefalvay, 2015.

"""
example_threshold is a brief example of processpathway that demonstrates the power of live processing: a whole
processing pipeline, with display functionality and other goodies, including threading, can be written in a few lines.
"""

import cv2
from processpathway.processpathway.process import LiveProcess

def convert_to_grayscale(_frame):
    _frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
    return _frame

def threshold(_frame):
    _, _frame = cv2.threshold(_frame, 128, 255, cv2.THRESH_BINARY)
    return _frame

def reconvert_to_bgr(_frame):
    _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2BGR)
    return _frame

if __name__ == '__main__':
    processor = LiveProcess(fps=True)
    processor.bind_process(convert_to_grayscale, threshold, reconvert_to_bgr)
    processor.initialise_capture_device(0)
    processor.loop()