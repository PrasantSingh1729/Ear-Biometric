import cv2
import time
from Canny import *
from earFeatureExtarction import *
from earShapeFinder import *
from earCompare import *
def getFvAndShape(img_path):
    img = cv2.imread(img_path)
    resizeimg = resizeImage(img,600)
    _, canny = getCanny(resizeimg,blur=9)
    canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    ear1 = getEarInfo(canny,drawShape=0,drawFeature=0)
    return ear1

def compareImg(img1,img2):
    ear1 = getFvAndShape(img1)
    ear2 = getFvAndShape(img2)
    print(ear1)
    print(ear2)
    return compareEar(ear1['fv'],ear2['fv'],a=0.2)

if __name__=='__main__':
    start = time.time()
    ans = compareImg("img/compare/1.jpg","img/compare/1t.jpg")
    print(ans,"% matched")
    end = time.time()
    print("Time took:",end-start)
    cv2.waitKey(0)

