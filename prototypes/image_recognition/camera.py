"""
cam3.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.

This program opens a video stream, and shows it on the screen.
Hit escape to exit the program.
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=camera.resolution)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    image = frame.array
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == 27 & 0xFF:#ord("q"):
        cv2.destroyAllWindows()
        print("Video feed closed successfully.")
        break