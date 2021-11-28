import base64
import cv2
import numpy as np


def readb64(uri):
   try:
      encoded_data = uri.split(',')[1]
   except IndexError:
      encoded_data = uri
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img
