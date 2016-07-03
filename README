ProcessPathway
--------------

ProcessPathway is a nifty little tool that lets you play with image processing algorithms instead of wiring up your test
bench all day. It is designed to feed a video camera input (a webcam, usually) through any functions that can digest and
return a numpy matrix (think OpenCV).

How to use
==========

The `example_threshold.py` example, which - as the name suggests - thresholds the the webcam input, is a good example 
for what a typical ProcessPathway pipeline would look like:

```python
import cv2
from processpathway import LiveProcess
```
First, import the LiveProcess object from processpathway. You might want to also import whatever processing functions
you need.

```
def convert_to_grayscale(_frame):
    _frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
    return _frame

def threshold(_frame):
    _, _frame = cv2.threshold(_frame, 128, 255, cv2.THRESH_BINARY)
    return _frame

def reconvert_to_bgr(_frame):
    _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2BGR)
    return _frame
```

Write your functions. The only constraint is that they should take and emit a numpy.ndarray image. Of course, that does 
not mean you can't code whatever side effects you need them to generate!

```
if __name__ == '__main__':
    processor = LiveProcess(fps=True)
    processor.bind_process(convert_to_grayscale, threshold, reconvert_to_bgr)
    processor.initialise_capture_device(0)
    processor.loop()
```

Upon call, attach `LiveProcess` to a variable, then bind the processing functions to it, *in the order you want them to 
be performed*! Then, bind a capture device and initialise it. Finally, start the loop.

Built-in functionalities
========================

* FPS calculation (use `fps=True` when constructing your `LiveProcess` instance)
* Screenshotting (bound to the `s` key, on by default but can be disabled using `screencap=False` in the `LiveProcess`
constructor
* Automatic clean-up and closedown (using the `esc` key by default)
* And lots more...

Todos
=====

* Tests!
* Documentation!
