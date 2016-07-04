# coding=utf-8

# ${PROJECTNAME}
# (c) Chris von Csefalvay, 2015.

"""
test_FPS is responsible for [brief description here].
"""
from time import sleep
from unittest import TestCase

from processpathway import FPS


class TestFPS(TestCase):
    def setUp(self):
        self.fpsc = FPS()

    def test_update(self):
        self.fpsc.update()
        sleep(1)
        self.fpsc.update()
        self.assertAlmostEqual(self.fpsc.fps, 1.0, places=2)
