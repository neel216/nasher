#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2


def order_points(pts):
    """
    Given an unordered set of points in a contour, this sorts the points by their relative position and
    returns a tuple, reorganized in the form (top-left, top-right, bottom-right, bottom-left). 
    
    :param pts: the tuple of points to be reordered.
    :return: a tuple, containing the same points, in a consistent order as described above.
    """
    
    # create an empty list to store the sorted coordinates; this is a list of 4 (x,y) coordinates. 
    rect = np.zeros((4,2), dtype = "float32")
    
    # compute an array s, containing the (x+y) sums of each coordinate.
    s = np.sum(np.sum(pts, axis=1), axis=1)
    
    # find the index of the coordinate pair with the minimum (x+y) sum - this will be the top left point.
    rect[0] = pts[np.argmin(s)]
    # find the index of the coordinate pair with the maximum (x+y) sum - this will be the bottom right point.
    rect[2] = pts[np.argmax(s)]

    # compute an array diff, containing the (x-y) differences of each coordinate.
    #diff = np.diff(pts, axis = 1)
    diff = np.diff(np.sum(pts, axis=1), axis=1)
    
    # find the index of the coordinate pair with the minimum (x-y) difference - this will be the top right point.
    rect[1] = pts[np.argmin(diff)]
    # find the index of the coordinate pair with the maximum (x-y) difference - this will be the bottom left point.
    rect[3] = pts[np.argmax(diff)]

    # return the populated, sorted tuple.
    return rect

def four_point_transform(image, pts):
    """
    Given an image and a set of coordinates, applies a perspective transform to the area bounded by the coordinates.
    The perspective transform processes the image, which may be taken at an angle, to reproduce what a top-down view would look like.
    
    :param image: the image to be processed
    :param pts: the tuple of coordinates within the image, to which the perspective transform will be applied. 
    :return: a new image, which respresents a top-down view of the specified region in the original image. 
    """
    
    # obtain the set of ordered points, then unpack them.
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    #print((tl, tr, br, bl))

    # calculate the width of the transformed image; this should be the greater of 
    # the distance between the bottom-right and bottom-left, and the distance between the top-right and top-left.
    w1 = ((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2)
    w2 = ((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2)
    #print((w1, w2))
    widthA = w1**0.5
    widthB = w2**0.5
    maxWidth = max(int(widthA), int(widthB))

    # calculate the height of the transformed image; this should be the greater of 
    # the distance between the top-right and bottom-right, and the distance between the top-left and bottom-left.
    h1 = ((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2)
    h2 = ((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2)
    #print((h1, h2))
    heightA = h1**0.5
    heightB = h2**0.5
    maxHeight = max(int(heightA), int(heightB))
    
    # create a set of coordinates for a rectangle, that the original image will fit into once transformed.
    dat = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # Apply the perspective transform to the image
    M = cv2.getPerspectiveTransform(rect, dat)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # Return the transformed image.
    #cv2.imwrite("pt_out.png", warped)
    return warped

def resize(img, res):
    """
    Resizes an image to a new resolution, while maintaining aspect ratio. 
    
    :param img: the image to be resized.
    :param res: the resolution to which the image should be resized. 
    :return: a new image with the specified resolution. 
    """
    
    # Unpack the widths and heights of both the resolution and image.
    # print(img.shape)
    (resW, resH) = (res[0], res[1])
    (imgX, imgY) = (img.shape[0], img.shape[1])

    # if the aspect ratio for the image is taller than the resolution's aspect ratio, resize the image along the y-axis.
    # if not, resize along the X-axis.
    if imgY/imgX > resH/resW: # imgX > imgY:
        outX = resW
        outY = imgY * (outX / imgX)
    else:
        outY = resH
        outX = imgX * (outY / imgY)

    # resize image to specified dimensions, then return image.
    dim = (int(outX), int(outY))
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def border(img, res): # fills in gaps on sides, maintaining original resolution
    """
    Adds black borders to a given image, so that the resulting image matches the specified resolution. 
    
    :param img: the image to which borders should be added
    :param res: a resolution, to which the image's borders should be extended
    :return: the original image with black borders
    """
    
    # unpack the widths and heights of the image and the desired resolution. 
    (imgX, imgY) = (img.shape[0], img.shape[1])
    (resW, resH) = (res[0], res[1])
    
    # compute the margins for the borders to fill (these are equal on both sides of the image).
    left = int(np.abs((resW - imgX) / 2))
    right = left
    top = int(np.abs((resH - imgY) / 2))
    btm = top

    # if the top margin is greater than 1, add borders to the top and bottom of image.
    if top > 1:
        e = np.full((resW,int(top/2),3), 0, dtype=np.uint8)
    
    # if the left margin is greater than 1, add borders to the left and right of the image.
    if left > 1:
        e = np.full((int(left/2),resH,3), 0, dtype=np.uint8)
        img = np.append(e, img[:][0])
        img = np.append(img[:][-1], e)
       
    # return the bordered image
    # print(img.shape)
    return img # cv2.copyMakeBorder(img, top, btm, left, right, cv2.BORDER_CONSTANT, value = (0, 0, 0))#[left:(resW - right), top:(resH - btm)]


if __name__ == '__main__':
    """
    As the methods in this transform module will be imported to our main code, the code below will not run; it is here only for testing purposes. 
    """
    order_points([[283, 224], [276, 264], [313, 263], [320, 231]])
    order_points([[462, 223], [435, 224], [433, 248], [455, 247]])
    np.argmax(np.sum([[462, 223], [435, 224], [433, 248], [455, 247]], axis=1))
