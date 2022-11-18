from Canny import *
from earFeatureExtarction import *
import math

def middlePoint(points):
    '''
    returns center point of the line joining points[0] and points[1]
    '''
    x1 , y1 = points[0]
    x2 , y2 = points[1]
    x3 = int((x2+x1)/2)
    y3 = int((y1+y2)/2)
    return [x3,y3]

def getOuterEdgeImg(canny,outeredge):
    outerEdgeImg = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    for point in outeredge:
        j , i = point
        outerEdgeImg[i][j]=255
    return outerEdgeImg

def getOverlapPercentage(img1,img2,edgeSize):
    ans = cv2.bitwise_and(img1,img2,mask=None)
    return cv2.countNonZero(ans)/edgeSize

def isFree(canny, lmax,refPoint, outerEdgeImg, edgeSize, draw=1):
    lobeMask = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    x1,y1 = middlePoint([lmax,refPoint])
    x2,y2 = lmax
    for i in range(y1,y2):
        for j in range(x2):
            lobeMask[i][j] = 255
    if(draw==1):
        cv2.rectangle(canny,[0,int((refPoint[1]+lmax[1])/2)],lmax,(0,255,255),1)

    if(getOverlapPercentage(lobeMask,outerEdgeImg,edgeSize)>0.03):
        return True
    else:
        return False
    
def isRound(canny, umax,refPoint,outerEdgeImg,edgeSize, draw=1):
    circleCenter = middlePoint([refPoint,umax])
    radius = int(math.dist(refPoint,umax)/2)
    circleMask = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    cv2.circle(circleMask,circleCenter,radius,(255),2)

    if(draw==1):
        cv2.circle(canny,circleCenter,radius,(255,0,255),1)
    
    if(getOverlapPercentage(circleMask,outerEdgeImg,edgeSize)>0.1):
        return True
    else:
        return False

def isNarrow(normalpoints, edgeSize):
    refLine = normalpoints[int(len(normalpoints)/2)]
    dist = math.dist(refLine[0],refLine[1])
    normalizeDist = dist/edgeSize
    if(normalizeDist<0.06):
        return True
    else:
        return False

def findShape(img,outerEdge,umax,lmax,normalpoints,draw=1):
    canny = img.copy()
    refLine = normalpoints[int(len(normalpoints)/2)]
    refPoint = refLine[0]

    outerEdgeImg = getOuterEdgeImg(canny,outerEdge)
    edgeSize = len(outerEdge)
    round = isRound(canny, umax,refPoint,outerEdgeImg,edgeSize)
    free = isFree(canny, lmax, refPoint, outerEdgeImg, edgeSize)
    narrow = isNarrow(normalpoints, edgeSize) 
    
    # ---------------------Drawings------------------------------------------
    cv2.circle(canny, umax, 2, (0,0,255), 2)
    cv2.circle(canny, lmax, 2, (0,0,255), 2)
    cv2.line(canny, umax,lmax,(0,0,255), 1)
    
    if(draw==1):
        cv2.imshow("Find Shape", canny)
    
    # print(free,round,narrow)

    return 4*free + 2*round + 1*narrow
    

if __name__=="__main__":
    # 195_ 020_ 014_ 033_ 035_t 038_ 065_
    # round - 195_ 014_
    # not round - 
    # attached - 014_
    # Free - 195_
    img_path = "img/195_.jpg"
    img = cv2.imread(img_path)
    resizeimg = resizeImage(img,500)
    gaussian, canny = getCanny(resizeimg,blur=9)
    
    canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    
    # importing canny image as 
    # img(in grayscale for processing) 
    # and canny(in RGB for drawing colorfull lines on it)
    grey = cv2.cvtColor(canny, cv2.COLOR_BGR2GRAY)
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

    shape = findShape(canny,outerEdge,umax,lmax,normalpoints)

    print("Category:",shape+1)
    print("Free Lobe:",bool(4&shape))
    print("Round:",bool(2&shape))
    print("Narrow:",bool(1&shape))

    cv2.imshow("original",resizeimg)
    cv2.waitKey(0)
    
    
    # img = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)