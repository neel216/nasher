"""
camera_transform.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.

Same as camera.py, but with the output processed under a Canny edge filter.
Contour tracking and highlights are added.
Minimal user input and perspective transform is added.
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
image = None
tran_img = None
tran_stage = 0  # 0: scanning, 1: captured / displaying original, 2: process original / display ptransform

def camera_init(cam, res):
    if cam.closed:
        cam = PiCamera()
    cam.resolution = res
    cam.framerate = 32
    # rawCapture = PiRGBArray(cam, size=cam.resolution)
    time.sleep(0.1)

def onMouse(event, x, y, flags, param):
    global tran_img, tran_stage, image, rawCapture # retrieve global vars

    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse input at: x = %d, y = %d'%(x, y))
        if tran_stage == 0:
            tran_stage += 1
            tran_img = image
            rawCapture.truncate(0)
            camera.close()
            print("Image captured. Click again to process and display perspective transform.")
        elif tran_stage == 1:
            tran_stage += 1
            print("Image processed. Click again to return to scanning mode.")
        elif tran_stage == 2:
            tran_stage = 0
            camera_init(camera, (640, 480))
            print("Returning to scanning mode.")


# camera and window initialization
camera = PiCamera()
camera_init(camera, (640, 480))
rawCapture = PiRGBArray(camera, size=camera.resolution)
window_title = "Video Feed"
cv2.namedWindow(window_title)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    image = frame.array
    edged = canny(image)
    cv2.setMouseCallback(window_title, onMouse)

    cont = find_contours(edged)
    if freeze_frame:  # if true, wait for keypress to advance to next frame.
        cv2.waitKey(0)
    outline_contours(window_title, image, cont, "RAW_CONTOURS")


    rawCapture.truncate(0) # refresh video feed buffer, to prepare for storing next frame.

    if cv2.waitKey(1) == 27 & 0xFF:  # registers Esc keypress, closes video feed and exits.
        cv2.destroyAllWindows()
        print("Video feed closed successfully.")
        break