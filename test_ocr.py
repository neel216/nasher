#from camera_ocr import run
#print("in test: {}".format(run()))

import time
s = time.time()


from tensorflow.keras.models import load_model

e = time.time()
elapse = e - s
print(elapse)