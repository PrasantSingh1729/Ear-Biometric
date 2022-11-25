import cv2
from Canny import *
from earFeatureExtarction import *
from earShapeFinder import *

if __name__=='__main__':
    # 195_ 020_ 014_ 033_ 035_t 038_ 065_
    # 029_t 0 6 7
    img_path = "img/195_.jpg"
    img = cv2.imread(img_path)
    resizeimg = resizeImage(img,500)
    gaussian, canny = getCanny(resizeimg,blur=9)
    
    canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    

    ear = getEarInfo(canny,drawShape=1,drawFeature=1)

    print("Feature Vector 1: (angle between reference_Line_1 joining reference point and normal intersection point on the outer edge)")
    print(len(ear['fv'][0]),"->",ear['fv'][0])
    print()
    print("Feature Vector 2: (angle between reference_line_2 joining reference point and normal intersection point on the outer edge)")
    print(len(ear['fv'][1]),"->",ear['fv'][1])
    print()
    print("Ear Category:",ear['shape']+1)
    print("Free Lobe:",bool(4&ear['shape']))
    print("Round:",bool(2&ear['shape']))
    print("Narrow:",bool(1&ear['shape']))

    # Display---------------------------------------------
    cv2.imshow("Original", resizeimg)
    cv2.imshow("Gaussian Blur", gaussian)
    cv2.imshow('Canny', canny)
    cv2.waitKey(0)

