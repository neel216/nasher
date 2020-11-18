#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2


def order_points(pts):
    rect = np.zeros((4,2), dtype = "float32")
    s = np.sum(np.sum(pts, axis=1), axis=1)
    s_min = np.argmin(s)
    s_max = np.argmax(s)
    #print("s_min")
    #print(s_min)
    #print("s_max")
    #print(s_max)
    rect[0] = pts[s_min]
    rect[2] = pts[s_max]
    #rect[0] = pts[np.min(len(pts)-1, np.argmin(s))]
    # rect[2] = pts[np.min(len(pts)-1, np.argmax(s))]

    #diff = np.diff(pts, axis = 1)
    diff = np.diff(np.sum(pts, axis=1), axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    #print((tl, tr, br, bl))

    w1 = ((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2)
    w2 = ((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2)
    #print((w1, w2))
    widthA = w1**0.5
    widthB = w2**0.5
    maxWidth = max(int(widthA), int(widthB))

    h1 = ((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2)
    h2 = ((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2)
    #print((h1, h2))
    heightA = h1**0.5
    heightB = h2**0.5
    maxHeight = max(int(heightA), int(heightB))

    dat = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dat)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    #cv2.imwrite("pt_out.png", warped)
    #print(warped)
    return warped

def resize(img, res):
    # print(img.shape)
    (resW, resH) = (res[0], res[1])
    (imgX, imgY) = (img.shape[0], img.shape[1])

    if imgY/imgX > resH/resW: # imgX > imgY:
        outX = resW
        outY = imgY * (outX / imgX)
    else:
        outY = resH
        outX = imgX * (outY / imgY)

    dim = (int(outX), int(outY))
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def border(img, res): # fills in gaps on sides, maintaining original resolution
    (imgX, imgY) = (img.shape[0], img.shape[1])
    (resW, resH) = (res[0], res[1])
    left = int(np.abs((resW - imgX) / 2))
    right = left
    top = int(np.abs((resH - imgY) / 2))
    btm = top

    if top > 1:
        e = np.full((resW,int(top/2),3), 0, dtype=np.uint8)
    elif left > 1:
        e = np.full((int(left/2),resH,3), 0, dtype=np.uint8)
        img = np.append(e, img[:][0])
        img = np.append(img[:][-1], e)
    print(img.shape)
    return img # cv2.copyMakeBorder(img, top, btm, left, right, cv2.BORDER_CONSTANT, value = (0, 0, 0))#[left:(resW - right), top:(resH - btm)]


if __name__ == '__main__':
    # order_points([[283, 224], [276, 264], [313, 263], [320, 231]])
    # order_points([[462, 223], [435, 224], [433, 248], [455, 247]])
    # np.argmax(np.sum([[462, 223], [435, 224], [433, 248], [455, 247]], axis=1))