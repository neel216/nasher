import numpy as np
import cv2
import imutils

def find_contours(img):
    cnts = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            # break
            return screenCnt


def outline_contours(win_name, img, contours, draw_type):
    if contours is not None:
        if draw_type == "RAW_CONTOURS":
            img = cv2.drawContours(img, [contours], -1, (255, 0, 0), 2)
        elif draw_type == "BOUNDING RECT":
            rect = cv2.minAreaRect(contours)
            box = np.int0(cv2.boxPoints(rect))
            img = cv2.drawContours(img, [box], -1, (255, 0, 0), 2)
    cv2.imshow(win_name, img)