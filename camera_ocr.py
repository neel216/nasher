#!/usr/bin/env python3
# coding: utf-8
'''
camera_ocr.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.
A script to launch a camera window, interpret any characters in the screen,
and return those characters as a string.
'''

import time
boot_start = time.time()

# Determine if we're on a Raspberry Pi or not
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    print('On Raspberry Pi')
    rpi = True
except ModuleNotFoundError:
    print('Not on Raspberry Pi')
    rpi = False
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
print("Boot time: {} seconds.".format(boot_end - boot_start))

# Load the character recognition model
mload_start = time.time()
model = load_model('data/handwriting.model', compile=False)
mload_end = time.time()
mload_dur = mload_end - mload_start
print("Model loading time: {} seconds.".format(mload_dur))


def camera_init(cam, res):
    '''
    Intializes a connected camera

    :param cam: a camera object to initialize. If on Raspbian, a PiCamera() object. If not on Raspbian, a cv2.VideoCapture() object
    :param res: the resolution for the camera
    :return: returns nothing
    '''
    if rpi:
        # If we're on a Raspberry Pi, initalize the PiCamera() object
        if cam.closed:
            cam = PiCamera()
        cam.resolution = res
        cam.framerate = 32
    else:
        # If we're not on a Raspberry Pi, initialize the resolution of a cv2.VideoCapture() object
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
    time.sleep(0.1) # small delay to allow camera to open


class CamOCR:
    '''
    Contains functions to interface with a camera, set up the user interface overlay for the camera,
    and run optical character recognition on a captured frame from the camera.
    '''
    def __init__(self):
        '''
        Constructs a CamOCR object.

        :return: returns nothing
        '''
        fullscreen = True
        self.freeze_frame = False
        self.resize_transform_out = True
        self.image = None
        self.ocr_img = None
        self.ocr_stage = 0  # 0: scanning, 1: captured / displaying original, 2: process original / display ptransform
        self.cont = []
        self.ocr_out = None

        # Set the pixel location and dimensions of the capture button overlay for the camera
        x1 = 30
        y1 = 380
        x2 = 480 - x1
        y2 = y1 + 80
        self.button = [y1 - 10, y2 - 10, x1 + 10, x2 - 10]

        # camera and window initialization
        if rpi:
            # Intialize a PiCamera() object if we're on Raspberry Pi
            self.camera = PiCamera()
            camera_init(self.camera, (640, 480))
            self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        else:
            # Initialize a cv2.VideoCapture() object if we're not a Raspberry Pi
            self.camera = cv2.VideoCapture(0)
            camera_init(self.camera, (640, 480))
        
        # Name the camera window and make it full screen
        self.window_title = "Camera"
        if fullscreen:
            cv2.namedWindow(self.window_title, cv2.WND_PROP_FULLSCREEN)
        else:
            cv2.namedWindow(self.window_title)
        cv2.setWindowProperty(self.window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # Run the onMouse() function if we register a click on the camera window
        cv2.setMouseCallback(self.window_title, self.onMouse)

    def onMouse(self, event, x, y, flags, param):
        '''
        Processes a mouse click on the camera window

        :param event: the click event that occurred
        :param x: the x position of the click
        :param y: the y position of the click
        :param flags: any flags passed from the click event
        :param param: any other parameters from the click event
        :return: returns nothing
        '''
        global ocr_img, ocr_stage, image, rawCapture, cont, model, ocr_out, camera # retrieve global vars

        # If the click was made by a left click and the click was on the capture button
        if event == cv2.EVENT_LBUTTONDOWN and y > self.button[0] and y < self.button[1] and x > self.button[2] and x < self.button[3]:
            # If we were on the camera stream
            if self.ocr_stage == 0:
                self.ocr_stage += 1
                self.ocr_out = process_ocr(model, image) # process the frame that was captured
                # Change the button text to read 'Exit Camera'
                image[self.button[0]:self.button[1], self.button[2]:self.button[3]] = 180
                cv2.putText(image, 'Exit Camera', (self.button[2] + (3 * int((self.button[3] - self.button[2]) / 32)), self.button[0] + (3 * int((self.button[1] - self.button[0]) / 4))), cv2.FONT_HERSHEY_PLAIN, 3, (0), 3)
                cv2.imshow(self.window_title, image)
                print("Image captured and processed. Click again to review information.")
            # If we were viewing the OCR results
            elif self.ocr_stage == 1:
                self.ocr_stage += 1
                if self.ocr_out is not None:
                    print("OCR Read: {}".format(self.ocr_out))

    def run(self):
        '''
        Opens the camera stream to take a picture

        :return: returns nothing
        '''
        global ocr_img, ocr_stage, image, rawCapture, cont, ocr_out # retrieve global vars

        if self.ocr_out is not None:
            return self.ocr_out

        v = self.ocr_stage < 3

        if rpi:
            # If we're on the Raspberry Pi, use the PiCamera() built in infinite iterator to display frames
            for frame in self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=v):
                if self.freeze_frame:  # if true, wait for keypress to advance to next frame.
                    cv2.waitKey(0)

                # If we're in the camera stream (we haven't taken a picture yet)
                if(self.ocr_stage == 0):
                    rot = cv2.rotate(frame.array, cv2.ROTATE_90_CLOCKWISE) # rotate the image
                    image = rot

                    # Overlay the capture button onto the image
                    image[self.button[0]:self.button[1], self.button[2]:self.button[3]] = 180
                    cv2.putText(image, 'Take Picture', (self.button[2] + (3 * int((self.button[3] - self.button[2]) / 32)), self.button[0] + (3 * int((self.button[1] - self.button[0]) / 4))), cv2.FONT_HERSHEY_PLAIN, 3, (0), 3)
                    
                    cv2.imshow(self.window_title, image)

                self.rawCapture.truncate(0) # refresh video feed buffer to prepare for storing next frame.

                # Registers Esc keypress, closes video feed and exits.
                if (cv2.waitKey(1) == 27 & 0xFF) | (self.ocr_stage == 2):
                    time.sleep(1)
                    self.camera.close()
                    cv2.destroyAllWindows()
                    print("Video feed closed successfully.")
                    if self.ocr_out is not None:
                        return self.ocr_out
                    else:
                        return None # on user exit, return no string.
                    break
        else:
            # If we're not on the Raspberry Pi, read frames from the camera until we break the loop
            while True:
                ret, frame = self.camera.read() # collect any errors and the frame from the camera
                if not ret:
                    print("Failed to grab frame")
                    break
                
                if self.freeze_frame:  # if true, wait for keypress to advance to next frame.
                    cv2.waitKey(0)

                # If we're in the camera stream (we haven't taken a picture yet)
                if(self.ocr_stage == 0):
                    image = frame
                    
                    # Overlay the capture button onto the image
                    image[self.button[0]:self.button[1], self.button[2]:self.button[3]] = 180
                    cv2.putText(image, 'Take Picture', (self.button[2] + (3 * int((self.button[3] - self.button[2]) / 32)), self.button[0] + (3 * int((self.button[1] - self.button[0]) / 4))), cv2.FONT_HERSHEY_PLAIN, 3, (0), 3)
                    
                    cv2.imshow(self.window_title, image)
                
                # registers Esc keypress, closes video feed and exits.
                if (cv2.waitKey(1) == 27 & 0xFF) | (self.ocr_stage == 2):

                    time.sleep(1)
                    self.camera.release()
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