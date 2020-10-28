"""
camera_contour.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.

Same as camera.py, but with the output processed under a Canny edge filter.
Contour tracking and highlights are added.
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from canny import canny

from contours import find_contours
from contours import outline_contours
import imutils

freeze_frame = False

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=camera.resolution)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    image = frame.array
    edged = canny(image)

    cont = find_contours(edged)
    if freeze_frame:  # if true, wait for keypress to advance to next frame.
        cv2.waitKey(0)
    outline_contours("Video Feed", image, cont, "RAW_CONTOURS")


    rawCapture.truncate(0) # refresh video feed buffer, to prepare for storing next frame.

    if cv2.waitKey(1) == 27 & 0xFF:  # registers Esc keypress, closes video feed and exits.
        cv2.destroyAllWindows()
        print("Video feed closed successfully.")
        break