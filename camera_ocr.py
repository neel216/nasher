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






class CamOCR():
    def __init__(self):
        self.fullscreen = True
        self.freeze_frame = False
        self.resize_transform_out = True
        self.image = None
        self.ocr_img = None
        self.ocr_stage = 0  # 0: scanning, 1: captured / displaying original, 2: process original / display ptransform
        self.cont = []
        self.ocr_out = None
        y1 = 464 - 50
        y2 = y1 + 40
        x1 = 116
        x2 = x1 + 200
        self.button = [y1, y2, x1, x2]

        # camera and window initialization
        self.camera = PiCamera()
        camera_init(self.camera, (640, 480))
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.window_title = "Camera"
        if self.fullscreen:
            cv2.namedWindow(self.window_title, cv2.WND_PROP_FULLSCREEN)
        else:
            cv2.namedWindow(self.window_title)
        cv2.setWindowProperty(self.window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback(self.window_title, self.onMouse)

    def onMouse(self, event, x, y, flags, param):
        global ocr_img, ocr_stage, image, rawCapture, cont, model, ocr_out, camera # retrieve global vars

        if event == cv2.EVENT_LBUTTONDOWN and y > self.button[0] and y < self.button[1] and x > self.button[2] and x < self.button[3]:
            if self.ocr_stage == 0:
                self.ocr_stage += 1
                self.ocr_out = process_ocr(model, image)
                cv2.imshow(self.window_title, image)
                print("Image captured and processed. Click again to review information.")
            elif self.ocr_stage == 1:
                self.ocr_stage += 1
                if self.ocr_out is not None:
                    print("OCR Read: {}".format(self.ocr_out))
                #print("Returning to scanning mode.")

    def run(self):
        global ocr_img, ocr_stage, image, rawCapture, cont, ocr_out # retrieve global vars

        if self.ocr_out is not None:
            return self.ocr_out

        v = self.ocr_stage < 3
        for frame in self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=v):

            #if ocr_out is not None:
            #    return ocr_out

            if self.freeze_frame:  # if true, wait for keypress to advance to next frame.
                cv2.waitKey(0)

            if(self.ocr_stage == 0):
                rot = cv2.rotate(frame.array, cv2.ROTATE_90_CLOCKWISE)
                image = rot
                image[self.button[0]:self.button[1], self.button[2]:self.button[3]] = 180
                cv2.imshow(self.window_title, image)

            self.rawCapture.truncate(0) # refresh video feed buffer, to prepare for storing next frame.

            if (cv2.waitKey(1) == 27 & 0xFF) | (self.ocr_stage == 2):  # registers Esc keypress, closes video feed and exits.

                #self.rawCapture.truncate(0)
                time.sleep(1)
                self.camera.close()
                cv2.destroyAllWindows()
                print("Video feed closed successfully.")
                if self.ocr_out is not None:
                    return self.ocr_out
                else:
                    return None # on user exit, return no string.
                break


if __name__ == "__main__":
    cam = CamOCR()
    cam.run()