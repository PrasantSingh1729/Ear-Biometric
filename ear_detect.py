import skimage.io as imageio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
left_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')
right_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')

cap = cv2.VideoCapture(0)
offset = 10
while True:
    success, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image",gray)

    Lears= left_ear_cascade.detectMultiScale(gray, 1.3, 5)
    if len(Lears):
        Lear = Lears[0]
        x,y,w,h = Lear
        cv2.rectangle(gray, (x-offset, y-offset), (x+w+offset, y+h+offset), (0, 255, 0), 2)
        Lcrop = img[y-offset:y+h+offset, x-offset:x+w+offset]
        cv2.imshow("Left Ear", cv2.Canny(Lcrop,60,120))

    Rears= right_ear_cascade.detectMultiScale(gray, 1.3, 5)
    if len(Rears):
        Rear = Rears[0]
        x,y,w,h = Rear
        cv2.rectangle(gray, (x-offset, y-offset), (x+w+offset, y+h+offset), (0, 255, 0), 2)
        Rcrop = img[y-offset:y+h+offset, x-offset:x+w+offset]
        cv2.imshow("Right Ear", cv2.Canny(Lcrop,60,120))
        

    cv2.imshow("Image", gray)
    # cv2.imshow("Image",cv2.Canny(gray,60,120))
    cv2.waitKey(1)