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


# left_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')
# right_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')
# offset = 10

img_path = "img/195_.jpg"
img = cv2.imread(img_path)
img = resizeImage(img,700)
cv2.imshow("Original", img)
img = cv2.GaussianBlur(img,(9,9),0) # odd size matrix is used
canny = cv2.Canny(img,60,120)
kernel = np.ones((2, 2), np.uint8)
img_dilation = cv2.dilate(canny, kernel, iterations=1)
cv2.imshow("Gaussian Blur", img)
cv2.imshow("canny", canny)
cv2.imshow("dilated canny", img_dilation)
# cv2.imwrite('canny/'+img_path, canny)
cv2.waitKey(0)