#from camera_ocr import run
#print("in test: {}".format(run()))

import time
s = time.time()


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

e = time.time()
elapse = e - s
print(elapse)