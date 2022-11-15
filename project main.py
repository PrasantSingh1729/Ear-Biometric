import cv2
from Canny import *
from earFeatureExtarction import *
if __name__=='__main__':
    img_path = "img/195_.jpg"
    img = cv2.imread(img_path)
    resizeimg = resizeImage(img,500)
    gaussian, canny = getCanny(resizeimg)
    
    canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    

    fvimg, fv1, fv2 = getFeatureVector(canny)

    
    print("Feature Vector 1: (angle between reference_Line_1 joining reference point and normal intersection point on the outer edge)")
    print(len(fv1),"->",fv1)
    print("Feature Vector 2: (angle between reference_line_2 joining reference point and normal intersection point on the outer edge)")
    print(len(fv2),"->",fv2)

    # Display---------------------------------------------
    cv2.imshow("Original", resizeimg)
    cv2.imshow("Gaussian Blur", gaussian)
    cv2.imshow('Canny', canny)
    cv2.imshow('Canny with Feature vector Drawings', fvimg)
    cv2.waitKey(0)

