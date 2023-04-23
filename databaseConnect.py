import pymongo
import random
from dummyGen import getDummyFeatureVector

import cv2
import time
from cannyAndGauss import *
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

def findPerson(fv):
    for item in collection.find():
        if compareEar(fv,item['fv'],a=0.1)>85:
            return item
    return -1

if __name__=='__main__':
    # print(getDummyFeatureVector())
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    # print(client)
    db = client['earBiometricDatabase']
    collection = db['earCollection']

    img = "img/register/prasant/3.jpeg"
    ear = getFvAndShape(img)
    person = findPerson(ear['fv'])
    if(person==-1):
        print("Access Denied")
    else:
        print("Thank you",person['name'])
