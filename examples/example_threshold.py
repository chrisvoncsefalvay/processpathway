# coding=utf-8

# 
# (c) Chris von Csefalvay, 2015.

"""
example_threshold is responsible for [brief description here].
"""

import cv2
from processpathway.processpathway.process import LiveProcess

def func1(_frame):
    _frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
    return _frame

def func2(_frame):
    _, _frame = cv2.threshold(_frame, 128, 255, cv2.THRESH_BINARY)
    return _frame

def func3(_frame):
    _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2BGR)
    return _frame

if __name__ == '__main__':
    processor = LiveProcess(fps=True)
    processor.bind_process(func1, func2)
    processor.initialise_capture_device(0)
    processor.loop()