from turtle import shape
import cv2
import numpy as np

def resizeImage(img,size):
    w = int(img.shape[1])
    h = int(img.shape[0])
    if w>h:
        h = int(min(h,size*h/w))
        w = int(min(size,w))
    else:
        w = int(min(w,size*w/h))
        h = int(min(size,h))
    img = cv2.resize(img,(w,h))
    return img

img_path = "img/009_.jpg"
image = cv2.imread(img_path,0)
image = resizeImage(image, 700)

cv2.imshow("input", image)
image = cv2.GaussianBlur(image,(3,3),0)
cv2.imshow("gaussian blur",image)
# canny = cv2.Canny(image,60,120)
canny = cv2.Canny(image,60,120)
kernel = np.ones((2, 2), np.uint8)
img_dilation = cv2.dilate(canny, kernel, iterations=1)
cv2.imshow("dilated", img_dilation)
cv2.imshow("canny", canny)
cv2.imwrite('canny/'+img_path, canny)
cv2.waitKey(0)