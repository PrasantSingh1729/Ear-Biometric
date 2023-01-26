import math
import numpy as np
import cv2
from earFeatureExtarction import *
from Canny import *

def getSlope(point1, point2):
    '''
    point1 = [x1,y1] \n
    point2 = [x2,y2] \n
    This funtion will return slope of line joining these two points.
    '''
    x1 , y1 = point1
    x2 , y2 = point2
    m = (y2-y1)/((x2-x1) if (x2-x1)!=0 else 1)
    return m

def getOuterEdgeImg(canny,outeredge):
    outerEdgeImg = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    for point in outeredge:
        j , i = point
        outerEdgeImg[i][j]=255
    return outerEdgeImg

def getOverlapPercentage(img1,img2,edgeSize,draw=1):
    ans = cv2.bitwise_and(img1,img2,mask=None)
    if draw==1:
        cv2.imshow('overlap',ans)
    return cv2.countNonZero(ans)/edgeSize

def getEllipseMask(canny,umax,refLine, draw=1):
    refPoint = refLine[0]
    ellipseMask = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    ellipseCenter = refPoint
    axesLength = (int(math.dist(umax,refPoint)), int(math.dist(refLine[0],refLine[1]))) 
    angle = math.degrees(math.atan(getSlope(umax,refPoint)))
    startAngle = 0
    endAngle = 360
    cv2.ellipse(ellipseMask,ellipseCenter,axesLength,angle,startAngle,endAngle,(255,0,255),3)

    if(draw==1):
        cv2.ellipse(canny,ellipseCenter,axesLength,angle,startAngle,endAngle,(255,0,255),3)
    
    return ellipseMask

def findShape(img,outerEdge,umax,lmax,normalpoints,draw=1):
    canny = img.copy()
    refLine = normalpoints[int(len(normalpoints)/2)]
    outerEdgeImg = getOuterEdgeImg(canny,outerEdge)
    edgeSize = len(outerEdge)

    
    ellipseMask = getEllipseMask(canny,umax,refLine,draw)
    overlapPercentage = getOverlapPercentage(outerEdgeImg,ellipseMask,edgeSize,draw)
    axesLength = (int(math.dist(umax,refPoint)), int(math.dist(refLine[0],refLine[1])))
    print(overlapPercentage)
    print(axesLength)
    print("ratio",axesLength[1]/axesLength[0])
    
    if(draw==1):
        cv2.circle(canny, umax, 2, (0,0,255), 2)
        cv2.circle(canny, lmax, 2, (0,0,255), 2)
        cv2.line(canny, umax,lmax,(0,0,255), 1)
        cv2.imshow('ellipseMask',ellipseMask)
        cv2.imshow('shape',canny)

   

if __name__=="__main__":

    # Triangular : 023_, 014_
    # Round: 
    # Oval:
    # Rectangular: 
    img_path = "img/Dataset/195_.jpg"
    img = cv2.imread(img_path)
    resizeimg = resizeImage(img,500)
    gaussian, canny = getCanny(resizeimg,blur=9)
    if canny is None:
        raise Exception("Image not Found")
    grey = canny.copy()
    canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    # Dilate the image to avoid error beacause of thin disjoints
    kernel = np.ones((2, 2), np.uint8)
    grey = cv2.dilate(grey, kernel, iterations=1)
    canny = cv2.dilate(canny, kernel, iterations=1)


    # Finding all connected line of white color in image
    # lines variable will have list of pixles(coordinates [x,y]) of all the lines present in the img
    lines = find_lines(grey)

    # Out of all the lines we need only the outer edge for further calculation
    # OuterEdge variable will consisit all the pixles of outer edge
    outerEdge = sorted(lines,key=len,reverse=True)[0]

    # Find furthest point on outer edge
    # umax - uppermost point
    # lmax - lowermost point 
    umax, lmax = furthestPoint(outerEdge)

    # Generating 19 points in between umax and lmax
    points = getPoints([umax, lmax],19)

    # Finding the intersection of normal drawn with outer edge
    normalpoints = createNormals(outerEdge, points)

    # Finding the reference point for feature vector 1
    # reference point is middle point
    refPoint = points[int(len(points)/2)]  

    # Finding feature vector 1
    fv1 = extractFeature(refPoint,normalpoints)





    # midline start and end point
    midLine = normalpoints[int(len(normalpoints)/2)]

    # finding middlePoint from start and end point of midline
    midPoint = middlePoint(midLine)

    # finding lmax2 by extanding line from 
    # umax to midpoint and find where it intersect on outeredge
    lmax2 = getLMax2(umax,midPoint,outerEdge)

    # Finding 9 points in between umax and lmax2
    points2 = getPoints([umax, lmax2],9)

    # Finding normal intersection point
    normalpoints2 = createNormals(outerEdge, points2)

    # Finding reference point for feature vector 2
    refPoint2 = points2[int(len(points2)/2)]

    # Finding the feature vector 2
    fv2 = extractFeature(refPoint2,normalpoints2)

    # midline start and end point
    midLine2 = normalpoints2[int(len(normalpoints2)/2)]

    findShape(canny,outerEdge,umax,lmax,normalpoints,draw=1)
    cv2.imshow('Original', resizeimg)
    cv2.imshow('canny', canny)
    cv2.waitKey(0)
