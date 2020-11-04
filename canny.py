"""
canny_class.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.
"""

import numpy as np
import cv2
import imutils

def canny(image, mode="auto"):

    # bw = cv2.threshold(image, 0, 20, cv2.THRESH_BINARY_INV)[1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    #blurred = cv2.fastNlMeansDenoising(10, 10, 7, 21)
    # blurred  = cv2.Laplacian(gray, cv2.CV_8U)
    # blurred = blurred / blurred.max()

    #blurred = cv2.threshold(blurred, 45, 255, cv2.THRESH_BINARY)[1]
    #blurred = cv2.erode(blurred, None, iterations=2)
    #blurred = cv2.dilate(blurred, None, iterations=2)

    #rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
    #sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17,17))
    #gradX = cv2.Sobel(gray, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=-1)
    #blurred = cv2.morphologyEx(gradX, cv2.MORPH_OPEN, rectKernel)
    # blurred = cv2.morphologyEx(gradX, cv2.MORPH_DILATE, sqKernel)
    # return cv2.threshold(blurred, 0, 20, cv2.THRESH_BINARY_INV)[1]


    if mode == "auto":
        sigma = 0.33 # 0.33
        v = np.median(blurred)

        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        return cv2.Canny(blurred, lower, upper)

    if mode == "wide":
        return cv2.Canny(blurred, 10, 200)

    if mode == "tight":
        return cv2.Canny(blurred, 255, 250)