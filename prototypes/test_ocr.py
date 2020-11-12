#from camera_ocr import run
from camera_ocr import CamOCR
from time import sleep

camList = []

camList.append(CamOCR())
print("in test: {}".format(camList[-1].run()))
sleep(10)
print("continue")

camList.append(CamOCR())
print("in test: {}".format(camList[-1].run()))

"""
import time
s = time.time()


from tensorflow.keras.models import load_model

e = time.time()
elapse = e - s
print(elapse)
"""