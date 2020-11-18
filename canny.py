#!/usr/bin/env python3
# coding: utf-8
'''
canny.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.
'''

import numpy as np
import cv2
import imutils


def canny(image, mode="auto"):
    '''
    Runs a Canny filter across a given image

    :param image: the image to run the Canny filter across
    :param mode: the mode that defines what resolution the Canny filter uses to process the image
    :return: the processed image
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert the image to grayscale
    blurred = cv2.GaussianBlur(gray, (3, 3), 0) # perform a Gaussian blur to get rid of noise

    if mode == "auto":
        # Automatically calculates the resolution of the Canny Filter based on the image
        sigma = 0.33 # 0.33
        v = np.median(blurred)

        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        return cv2.Canny(blurred, lower, upper)

    if mode == "wide":
        # Performs the Canny process using a wide resolution
        return cv2.Canny(blurred, 10, 200)

    if mode == "tight":
        # Performs the Canny process using a small resolution
        return cv2.Canny(blurred, 255, 250)