#!/usr/bin/env python3
# coding: utf-8

import cv2
import time
import numpy as np


#img = cv2.imread("/home/pi/Desktop/nasher/images/screenshot.png")

def find_decimals(img):
    '''
    Finds decimal points in a given image

    :param img: the image to process and find decimal points in
    :return: A list of coordinates that describe the location of each decimal point
    '''
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(img, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                   param2 = 10, minRadius = 1, maxRadius = 5)

    # Draw circles that are detected.
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        circ_out = []

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
            #cv2.imshow("Detected Circle", img)
            #cv2.waitKey(0)
            #circ_out.append([a, b]))
            circ_out.append([b, a])

        return circ_out

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    else:
        # If no circles are detected
        return None