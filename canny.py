from turtle import shape
import cv2
import numpy as np

img_path = "img/000_.jpg"
image = cv2.imread(img_path,0)

p = 500
w = int(p)
h = int(image.shape[0]/image.shape[1])*p
image = cv2.resize(image, (w, h))

cv2.imshow("input", image)
# image = cv2.GaussianBlur(image,(9,9),0)
# cv2.imshow("gaussian blur",image)
# canny = cv2.Canny(image,60,120)
canny = cv2.Canny(image,60,120)
kernel = np.ones((2, 2), np.uint8)
img_dilation = cv2.dilate(canny, kernel, iterations=1)
cv2.imshow("dilated", img_dilation)
cv2.imshow("canny", canny)
cv2.imwrite('canny/'+img_path, canny)
cv2.waitKey(0)