#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import cv2
import imutils

def find_contours(img):
    '''
    Finds the contours of edges in a given image

    :param img: a pre-processed image to find contours in
    :return: a polygon that has 4 sides (a rectangle)
    '''
    # Find contours in a pre-processed image and sort them
    cnts = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    screenCnt = []

    # For each contour found
    for c in cnts:
        peri = cv2.arcLength(c, True) # Calculate the length of each contour
        approx = cv2.approxPolyDP(c, 0.1 * peri, True) # Lower the resolution of the polygon to see what polygon is approximately resembles

        # If we find that the polygon has approximately 4 sides (it's a rectangle)
        if len(approx) == 4:
            screenCnt = approx
            #screenCnt.append(approx)
            return screenCnt

def outline_contours(img, contours, draw_type="RAW_CONTOURS"):
    '''
    Draws contours on a given image

    :param img: the image to draw the contours on
    :param contours: the contours the draw on the image
    :param draw_type: whether to outline the contours or draw rectangles around the contours
    :return: the image with contours drawn on it
    '''
    # If there are contours to draw
    if contours is not None:
        # If we want to outline the contours
        if draw_type == "RAW_CONTOURS":
            img = cv2.drawContours(img, [contours], -1, (255, 0, 0), 2)
            #for c in contours:
            #    img = cv2.drawContours(img, c, -1, (255, 0, 0), 2)
        # If we want to draw rectangles around the contours
        elif draw_type == "BOUNDING RECT":
            rect = cv2.minAreaRect(contours)
            box = np.int0(cv2.boxPoints(rect))
            img = cv2.drawContours(img, [box], -1, (255, 0, 0), 2)

    return img