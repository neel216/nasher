"""
canny_class.py
Author: Phillip Williams (pcw14)
Acknowledgements to Adrian Rosebrock of pyimagesearch.com for his
tutorials on AI and image processing.
"""

import numpy as np
import cv2

def canny(image, mode="auto"):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

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