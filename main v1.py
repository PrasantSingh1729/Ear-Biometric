import cv2
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


def dfs(img,visited,i,j):
    if(i<0 or j<0 or i>=len(visited) or j>=len(visited[0]) or visited[i][j]==np.bool_(True) or img[i][j]<100):
        return []
    visited[i][j] = 1
    return [[j,i]] + dfs(img, visited, i,j+1) + dfs(img, visited, i,j-1) + dfs(img, visited, i+1,j) + dfs(img, visited, i-1,j)

def find_lines(img):
    visited = np.zeros((img.shape[0],img.shape[1]), dtype=bool)
    lines = list()
    for i in range(len(img)):
        for j in range(len(img[0])):
            if(img[i][j]>100 and visited[i][j]==0):
                lines.append(dfs(img, visited,i,j))
    return lines

def furthestPoint(points):
    maxx = 0
    pair = tuple()
    for i in range(len(points)):
        for j in range (i+1,len(points)):
            dis = math.dist(points[i],points[j])
            if(dis>maxx):
                maxx = dis
                pair = (points[i],points[j])
    return pair

def getPoints(points, n):
    if n%2==0:
        raise Exception("Odd value for n is required")
    ans = list()
    d = math.dist(points[0],points[1])/(n+1)
    x1, y1 = points[1]
    x2, y2 = points[0]
    m = (y2-y1)/(x2-x1)
    c = y1 - m*x1
    for i in range(n):
        X1 = int(((1/math.sqrt(1+m**2))*(i+1)*d + x1))
        Y1 = int(((m/math.sqrt(1+m**2))*(i+1)*d + y1))
        ans.append([X1,Y1])
    return ans
    
def findIntersection(point1, m, outerEdge, sign=1):
    x1 , y1 = point1
    for d in range(1,300):
        x2 = int(((1/math.sqrt(1+m**2))*sign*d + x1))
        y2 = int(((m/math.sqrt(1+m**2))*sign*d + y1))
        if([x2,y2] in outerEdge):
            return [x2,y2]
    return []

def createNormals(outerEdge, points):
    x1 , y1 = points[0]
    x2 , y2 = points[1]
    m = (y2-y1)/(x2-x1)
    m = -1/m
    ans = list()
    for point1 in points:
        point2 = findIntersection(point1, m, outerEdge)
        if not len(point2)==0:
            ans.append([point1,point2])
    return ans

def middlePoint(points):
    x1 , y1 = points[0]
    x2 , y2 = points[1]
    x3 = int((x2+x1)/2)
    y3 = int((y1+y2)/2)
    return [x3,y3]

def getLmin2(img, umax,midPoint,outerEdge):
    x1 , y1 = umax
    x2 , y2 = midPoint
    m = (y2-y1)/(x2-x1)
    lmin2 = findIntersection(midPoint,m,outerEdge,-1)
    return lmin2


path = 'canny/img/001_.jpg'
img = cv2.imread(path,0)
img2 = cv2.imread(path)
kernel = np.ones((2, 2), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img2 = cv2.dilate(img2, kernel, iterations=1)

lines = find_lines(img)
outerEdge = sorted(lines,key=len,reverse=True)[0]

umax, lmin = furthestPoint(outerEdge)

cv2.circle(img2, umax, 2, (0,0,255), 2)
cv2.circle(img2, lmin, 2, (0,0,255), 2)
cv2.line(img2,umax,lmin,(0,0,255), 1)

points = getPoints([umax, lmin],19)
for x in points:
    cv2.circle(img2, x, 2, (0,255,0), 2)

refPoint = points[int(len(points)/2)]
cv2.circle(img2, refPoint, 2, (255,0,128), 2)


normalpoints = createNormals(outerEdge, points)
for point in normalpoints:
    cv2.line(img2,point[0],point[1],(255,0,0), 1)


midLine = normalpoints[int(len(normalpoints)/2)]
midPoint = middlePoint(midLine)
cv2.line(img2,midLine[0],midLine[1],(255,0,128), 1)
cv2.circle(img2, midPoint, 2, (0,255,0), 2)

lmin2 = getLmin2(img2, umax,midPoint,outerEdge)
cv2.circle(img2, lmin2, 2, (0,0,255), 2)
cv2.line(img2,umax,lmin2,(0,0,255), 1)

points2 = getPoints([umax, lmin2],9)
for x in points2:
    cv2.circle(img2, x, 2, (0,255,0), 2)

refPoint2 = points2[int(len(points2)/2)]

cv2.circle(img2, refPoint2, 2, (255,0,128), 2)
normalpoints2 = createNormals(outerEdge, points2)
for point in normalpoints2:
    cv2.line(img2,point[0],point[1],(255,255,0), 1)


cv2.imshow('Original', img)
cv2.imshow('Painted', img2)
cv2.waitKey(0)



# x2 = int(((1/math.sqrt(1+m**2))*100 + x1))
# y2 = int(((m/math.sqrt(1+m**2))*100 + y1))
# cv2.line(img, (x1,y1),(x2,y2),(255),2)