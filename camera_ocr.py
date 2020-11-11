"""
camera_ocr.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.

A script to launch a camera window, interpret any characters in the screen,
and return those characters as a string.
"""
import time
boot_start = time.time()

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from canny import canny
from contours import find_contours
from contours import outline_contours
from transform import order_points
from transform import four_point_transform
from transform import resize
from transform import border
from tensorflow.keras.models import load_model
from ocr import process_ocr
import imutils

boot_end = time.time()
boot_dur = boot_end - boot_start
print("Boot time: {} seconds.".format(boot_dur))

fullscreen = True
freeze_frame = False
resize_transform_out = True
image = None
ocr_img = None
ocr_stage = 0  # 0: scanning, 1: captured / displaying original, 2: process original / display ptransform
cont = []
ocr_out = None

mload_start = time.time()
model = load_model('/home/pi/production/nasher/data/handwriting.model', compile = False)
mload_end = time.time()
mload_dur = mload_end - mload_start
print("Model loading time: {} seconds.".format(mload_dur))

def camera_init(cam, res):
    if cam.closed:
        cam = PiCamera()
    cam.resolution = res
    cam.framerate = 32
    # rawCapture = PiRGBArray(cam, size=cam.resolution)
    time.sleep(0.1)

def onMouse(event, x, y, flags, param):
    global ocr_img, ocr_stage, image, rawCapture, cont, model, ocr_out, camera # retrieve global vars

    if event == cv2.EVENT_LBUTTONDOWN:
        if ocr_stage == 0:
            ocr_stage += 1
            ocr_out = process_ocr(model, image)
            cv2.imshow(window_title, image)
            print("Image captured and processed. Click again to review information.")
        elif ocr_stage == 1:
            ocr_stage += 1
            if ocr_out is not None:
                print("OCR Read: {}".format(ocr_out))
            #print("Returning to scanning mode.")


# camera and window initialization
camera = PiCamera()
camera_init(camera, (640, 480))
rawCapture = PiRGBArray(camera, size=camera.resolution)
window_title = "Camera"
if fullscreen:
    cv2.namedWindow(window_title, cv2.WND_PROP_FULLSCREEN)
else:
    cv2.namedWindow(window_title)
cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback(window_title, onMouse)

def run():
    global ocr_img, ocr_stage, image, rawCapture, cont, ocr_out # retrieve global vars

    if ocr_out is not None:
        return ocr_out

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

        #if ocr_out is not None:
        #    return ocr_out

        if freeze_frame:  # if true, wait for keypress to advance to next frame.
            cv2.waitKey(0)

        if(ocr_stage == 0):
            rot = cv2.rotate(frame.array, cv2.ROTATE_90_CLOCKWISE)
            image = rot
            cv2.imshow(window_title, image)

        rawCapture.truncate(0) # refresh video feed buffer, to prepare for storing next frame.

        if (cv2.waitKey(1) == 27 & 0xFF) | (ocr_stage == 2):  # registers Esc keypress, closes video feed and exits.
            cv2.destroyAllWindows()
            print("Video feed closed successfully.")
            if ocr_out is not None:
                return ocr_out
            else:
                return None # on user exit, return no string.


if __name__ == "__main__":
    run()