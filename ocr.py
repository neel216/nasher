#!/usr/bin/env python3
# coding: utf-8

from imutils.contours import sort_contours
import numpy as np
import imutils
import cv2


def process_ocr(model, frame, test=False):
    '''
    Processes an image using a handwriting recognition model to detect numbers in the image

    :param model: the Tensorflow Keras model used to make predictions on the image
    :param frame: the image to process and run predictions on
    :param test: whether the functions should be in testing mode or not
    :return: a string containing the numbers detect in the image
    '''
    image = frame

    # convert the image to grayscale, and perform a Gaussian blur
    # to reduce noise
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    '''
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=12, minRadius=0,maxRadius=20)
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(blurred, (i[0]. i[1]), i[2], (0,255,0), 2)
    '''

    # perform edge detection
    edged = cv2.Canny(blurred, 30, 50, apertureSize=3) # 30, 150 ; 10, 100, 5

    # find contours in the edge map, and sort the
    # resulting contours from left-to-right
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # If we found at least 1 number
    if len(cnts) > 0:
        #print(cnts)
        cnts = imutils.grab_contours(cnts)
        #print(cnts)
        cnts = sort_contours(cnts, method="left-to-right")[0]

        # initialize the list of contour bounding boxes and associated
        # characters that we'll be OCR'ing
        chars = []

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)

            # filter out bounding boxes, ensuring they are neither too small
            # nor too large
            if (w >= 5 and w <= 150) and (h >= 15 and h <= 120):
                # extract the character and threshold it to make the character
                # appear as *white* (foreground) on a *black* background, then
                # grab the width and height of the thresholded image
                roi = gray[y:y + h, x:x + w]
                thresh = cv2.threshold(roi, 0, 255,
                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                (tH, tW) = thresh.shape

                # if the width is greater than the height, resize along the
                # width dimension
                if tW > tH:
                    thresh = imutils.resize(thresh, width=32)

                # otherwise, resize along the height
                else:
                    thresh = imutils.resize(thresh, height=32)

                # re-grab the image dimensions (now that its been resized)
                # and then determine how much we need to pad the width and
                # height such that our image will be 32x32
                (tH, tW) = thresh.shape
                dX = int(max(0, 32 - tW) / 2.0)
                dY = int(max(0, 32 - tH) / 2.0)

                # pad the image and force 32x32 dimensions
                padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
                    left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
                    value=(0, 0, 0))
                padded = cv2.resize(padded, (32, 32))

                # prepare the padded image for classification via our
                # handwriting OCR model
                padded = padded.astype("float32") / 255.0
                padded = np.expand_dims(padded, axis=-1)

                # update our list of characters that will be OCR'd
                chars.append((padded, (x, y, w, h)))

        # extract the bounding box locations and padded characters
        boxes = [b[1] for b in chars]
        chars = np.array([c[0] for c in chars], dtype="float32")

        # OCR the characters using our handwriting recognition model
        preds = model.predict(chars)

        # define the list of label names
        labelNames = "0123456789"
        labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        labelNames = [l for l in labelNames]

        # loop over the predictions and bounding box locations together
        locs = []
        for (pred, (x, y, w, h)) in zip(preds, boxes):
            # find the index of the label with the largest corresponding
            # probability, then extract the probability and label
            i = np.argmax(pred)
            prob = pred[i]
            label = labelNames[i]

            # if the character is a number and we are more than 55% confident in the prediction
            if label in '0123456789' and prob > 0.55:
                # draw the prediction on the image
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, label,
                            (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                            (0, 255, 0), 2)
                locs.append([label, x])

        out = []
        # Return the number we detect
        for c in locs:
           out.append(str(c[0]))
        return "".join(out)
    else:
        # If we found 0 numbers
        return