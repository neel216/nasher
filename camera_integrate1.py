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
from transform import order_points
from transform import four_point_transform
from transform import resize
from transform import border
import imutils

freeze_frame = False
resize_transform_out = True
image = None
tran_img = None
tran_stage = 0  # 0: scanning, 1: captured / displaying original, 2: process original / display ptransform
cont = []

def camera_init(cam, res):
    if cam.closed:
        cam = PiCamera()
    cam.resolution = res
    cam.framerate = 32
    # rawCapture = PiRGBArray(cam, size=cam.resolution)
    time.sleep(0.1)

def onMouse(event, x, y, flags, param):
    global tran_img, tran_stage, image, rawCapture, cont # retrieve global vars

    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse input at: x = %d, y = %d'%(x, y))
        if tran_stage == 0:
            tran_stage += 1
            tran_img = image
            #rawCapture.truncate(0)
            print("Image captured and processed. Click again to review information.")
        elif tran_stage == 2:
            tran_stage += 1

            #print(type(cont[0][0][0]))
            tran_img = four_point_transform(tran_img, cont)
            #cv2.imshow(window_title, tran_img)

            print("Modify information? Click again to return to scanning mode.")
        elif tran_stage == 4:
            tran_stage = 0
            #cv2.imwrite("pt_out.png", tran_img)
            print("Returning to scanning mode.")


# camera and window initialization
camera = PiCamera()
camera_init(camera, (640, 480))
rawCapture = PiRGBArray(camera, size=camera.resolution)
window_title = "Video Feed"
cv2.namedWindow(window_title)
cv2.setMouseCallback(window_title, onMouse)

def run():
    global tran_img, tran_stage, image, rawCapture, cont # retrieve global vars

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        if(tran_stage == 0):
            image = frame.array

        if freeze_frame:  # if true, wait for keypress to advance to next frame.
            cv2.waitKey(0)

        if(tran_stage == 0):
            cv2.imshow(window_title, image)
        elif(tran_stage == 1):
            edged = canny(image)
            cont = find_contours(edged)
            #print(cont)
            tcont = []
            if cont is not None:
                for pair in cont:
                    tcont.append(pair[0])
                #print(np.ndarray(tcont))
                pts = np.array(cont, dtype = "float32")
                cntrd = outline_contours(image, cont, "RAW_CONTOURS")
                cv2.imshow(window_title, cntrd)
                # trfm = four_point_transform(image, pts)
                # cv2.imshow(window_title, tfrm)
                tran_stage += 1
            else:
                print("No closed contour detected: Returning to scanning mode.")
                tran_stage = 0

        elif(tran_stage == 3):
            #edged = canny(image)
            #cont = find_contours(edged)
            #cntrd = outline_contours(image, cont, "RAW_CONTOURS")
            # tran_img = np.array(four_point_transform(tran_img, cont), dtype=np.uint8)
            #rawCapture.truncate(0)
            if resize_transform_out == True:
                scale = resize(tran_img, camera.resolution)
                brdr = border(scale, camera.resolution)
                #brdr[50:70][:] = [0, 0, 255]
                cv2.imshow(window_title, scale)
                # cv2.imshow(window_title, brdr)
            else:
                cv2.imshow(window_title, tran_img)
            tran_stage += 1



        rawCapture.truncate(0) # refresh video feed buffer, to prepare for storing next frame.

        if cv2.waitKey(1) == 27 & 0xFF:  # registers Esc keypress, closes video feed and exits.
            cv2.destroyAllWindows()
            print("Video feed closed successfully.")
            break


if __name__ == "__main__":
    run()