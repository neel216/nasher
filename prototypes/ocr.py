#!/usr/bin/env python3
# coding: utf-8
'''
CREDIT: https://www.pyimagesearch.com/2020/08/24/ocr-handwriting-recognition-with-opencv-keras-and-tensorflow/
This file contains the code to read the handwritten text in an image
Specifically edited to apply towards reading the object number on a painting's tag
in the Nasher Museum's storage space

TODO: make better
sigma=0.33):
    v = np.median(image)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
'''
# USAGE - IGNORE THIS
# python ocr_handwriting.py --model handwriting.model --image images/umbc_address.png

# import the necessary packages
from tensorflow.keras.models import load_model
from imutils.contours import sort_contours
import numpy as np
import imutils
import cv2
from time import sleep, time

start_ = time()
# load the handwriting OCR model
print("[INFO] loading handwriting OCR model...")
model = load_model('../data/handwriting.model')
end_ = time()



test = False # if true, displays the image as each filter is applied. if false, skips straight to the prediction image



cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 464) # 320
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 464) # 180
img = None

while True:
	ret, frame = cam.read()
	if not ret:
		print("failed to grab frame")
		break
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(blurred, 30, 50, apertureSize=3)
	cv2.imshow("Canny", edged)
	#ret3, th3 = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#cv2.imshow('Otsu', th3)
	
	k = cv2.waitKey(1)
	if k % 256 == 27:
		# ESC pressed
		print("Escape hit, closing...")
		break
	elif k % 256 == 32:
		# SPACE pressed
		img = frame
		print('Picture taken!')
		break
        #img_name = "opencv_frame_{}.png".format(img_counter)
        #cv2.imwrite(img_name, frame)
        #print("{} written!".format(img_name))

cam.release()
cv2.destroyAllWindows()





start = time()
# load the input image from disk, convert it to grayscale, and blur
# it to reduce noise
path = '../images/raw2.jpg'
image = cv2.imread(path)
image = img
if test:
	cv2.imshow('Image', image)
	cv2.waitKey(0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
if test:
	cv2.imshow('Gray', gray)
	cv2.waitKey(0)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
if test:
	cv2.imshow('Blurred', blurred)
	cv2.waitKey(0)

# perform edge detection, find contours in the edge map, and sort the
# resulting contours from left-to-right
edged = cv2.Canny(blurred, 30, 50, apertureSize=3) # 30, 150 ; 10, 100, 5
if test:
	cv2.imshow('Canny', edged)
	cv2.waitKey(0)
#print(edged)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
Xs = []
Ys = []
nums = []
for (pred, (x, y, w, h)) in zip(preds, boxes):
	# find the index of the label with the largest corresponding
	# probability, then extract the probability and label
	i = np.argmax(pred)
	prob = pred[i]
	label = labelNames[i]

	if label in '0123456789':
		print("[INFO] {} - {:.2f}%".format(label, prob * 100))
	if label in '0123456789' and prob > 0.5:
		# draw the prediction on the image
		#print("[INFO] {} - {:.2f}%".format(label, prob * 100))
		nums.append((label, prob, x, y, w, h))
		Xs.append(x)
		Ys.append(y)

import statistics
y_median = statistics.median(Ys)

new = []
range_ = 0.2
for i in range(len(Ys)):
	if Ys[i] < y_median * (1 + range_) and Ys[i] > y_median * (1 - range_):
		new.append(nums[i])
		# show the image

cv2.rectangle(image, (0, int(y_median * ((1 - range_)))), (600, int(y_median * (1 + range_))), (255, 0, 0), 2)

for (label, prob, x, y, w, h) in new:
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.putText(image, label, (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

diff = set(new).symmetric_difference(set(nums))
for (label, prob, x, y, w, h) in diff:
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.putText(image, label, (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

end = time()
print(f'Time to load model: {end_ - start_} seconds')
print(f'Time to process image: {end - start} seconds')
print('Xs:', Xs)
print('Ys:', Ys)
cv2.imshow("Image", image)
cv2.waitKey(0)
