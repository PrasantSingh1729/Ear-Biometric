from weakref import ref
import cv2
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


def getSlope(point1, point2):
    x1 , y1 = point1
    x2 , y2 = point2
    # it may cause error
    m = (y2-y1)/(x2-x1) 
    m = (y2-y1)/((x2-x1) if not (x2-x1)==0 else 1)
    return m

def isSafe(img,visited, i, j):
    if(i<0 or i>=len(img) or j<0 or j>=len(img[0]) or visited[i][j]==1 or img[i][j]<100):
        return False
    else:
        return True

def bfs(img,visited,i,j):
    line_pixels = []
    queue = []
    visited[i][j] = 1
    queue.append([i,j])

    while queue:
        m = queue.pop(0)
        I, J = m
        line_pixels.append([J,I])
        if(isSafe(img,visited, I, J+1)):
            visited[I][J+1] = 1
            queue.append([I,J+1])
        if(isSafe(img,visited, I, J-1)):
            visited[I][J-1] = 1
            queue.append([I,J-1])
        if(isSafe(img,visited, I+1, J)):
            visited[I+1][J] = 1
            queue.append([I+1,J])
        if(isSafe(img,visited, I-1, J)):
            visited[I-1][J] = 1
            queue.append([I-1,J])
    return line_pixels

def dfs(img,visited,i,j,sign):
    if(i<0 or j<0 or i>=len(visited) or j>=len(visited[0]) or visited[i][j]==1 or img[i][j]<100):
        return []
    visited[i][j] = 1

    return [[j,i]] + dfs(img, visited, i,j+(sign),sign) + dfs(img, visited, i,j-(sign),sign) + dfs(img, visited, i+(sign),j,sign) + dfs(img, visited, i-(sign),j,sign)

def find_lines(img):
    # print(sign)
    visited = np.zeros((img.shape[0],img.shape[1]), dtype=bool)
    lines = list()
    for i in range(len(img)):
        for j in range(len(img[0])):
            if(img[i][j]>100 and visited[i][j]==0):
                # print(i,j)
                lines.append(bfs(img, visited,i,j))
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

def getsign(point1, point2):
    m = getSlope(point1,point2)
    prev = math.dist(point1,point2)
    x1, y1 = point1
    x2, y2 = point2
    x3 = int(((1/math.sqrt(1+m**2))*1*10 + x1))
    y3 = int(((m/math.sqrt(1+m**2))*1*10 + y1))
    curr = math.dist([x3,y3],point2)
    if(curr<prev):
        return 1
    else:
        return -1

def getPoints(points, n, sign=1):
    if n%2==0:
        raise Exception("Odd value for n is required")
    ans = list()
    d = math.dist(points[0],points[1])/(n+1)
    x1, y1 = points[1]
    x2, y2 = points[0]
    sign = int(getsign(points[1],points[0]))
    m = getSlope(points[0],points[1])
    c = y1 - m*x1
    for i in range(n):
        X1 = int(((1/math.sqrt(1+m**2))*(i+1)*sign*d + x1))
        Y1 = int(((m/math.sqrt(1+m**2))*(i+1)*sign*d + y1))
        ans.append([X1,Y1])
    if(not len(ans)==n):
        return getPoints(points,n,-1)
    return ans
    
def findIntersection(point1, m, outerEdge, sign):
    x1 , y1 = point1
    for d in range(4,300):
        x2 = int(((1/math.sqrt(1+m**2))*sign*d + x1))
        y2 = int(((m/math.sqrt(1+m**2))*sign*d + y1))
        if([x2,y2] in outerEdge):
            return [x2,y2]
    return []

def createNormals(outerEdge, points):
    m = getSlope(points[1],points[2])
    if not m==0:
        m = -1/m
    sign = 1
    ans = list()
    for point1 in points:
        point2 = findIntersection(point1, m, outerEdge, sign)
        if not len(point2)==0:
            ans.append([point1,point2])
    if(len(ans)==len(points)):
        return ans
    sign = -1
    ans = list()
    for point1 in points:
        point2 = findIntersection(point1, m, outerEdge, sign)
        if not len(point2)==0:
            ans.append([point1,point2])
    return ans

def middlePoint(points):
    x1 , y1 = points[0]
    x2 , y2 = points[1]
    x3 = int((x2+x1)/2)
    y3 = int((y1+y2)/2)
    return [x3,y3]

def getLMax2(umax,midPoint,outerEdge):
    m = getSlope(umax,midPoint)
    print("Slope:", m)
    lmax2 = findIntersection(midPoint,m,outerEdge,-1)
    if(lmax2[1]>midPoint[1]):
        return lmax2
    else:
        return findIntersection(midPoint,m,outerEdge,1)

def extractFeature(img, ref,normalpoints,precision=2):
    fv = list()
    m1 = getSlope(ref, normalpoints[int(len(normalpoints)/2)][1])
    # cv2.circle(img, normalpoints[int(len(normalpoints)/2)][1],5,(255,255,0),6);
    print("m1=",m1)
    for point in normalpoints:
        m2 = getSlope(ref, point[1])
        fv.append(round((m1-m2)/(1+m1*m2),precision))
    return fv



# importing canny image as 
# img(in grayscale for processing) 
# and img2(in RGB for drawing colorfull lines on it)
path = 'canny/img/195_.jpg'
img = cv2.imread(path,0) # second parameter is Zero indicate we want to import image in grayscale
img2 = cv2.imread(path)  

# Dilate the image to avoid error beacause of thin disjoints
kernel = np.ones((2, 2), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img2 = cv2.dilate(img2, kernel, iterations=1)


# Finding all connected line of white color in image
# lines variable will have list of pixles(coordinates [x,y]) of all the lines present in the img
lines = find_lines(img)

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
fv1 = extractFeature(img2, refPoint,normalpoints)

#------------Drawings for feature vector 1-------------------
cv2.circle(img2, umax, 2, (0,0,255), 2)
cv2.circle(img2, lmax, 2, (0,0,255), 2)
cv2.line(img2,umax,lmax,(0,0,255), 1)
for x in points:
    cv2.circle(img2, x, 2, (0,255,0), 2)
for point in normalpoints:
    cv2.line(img2,point[0],point[1],(255,0,0), 1)

cv2.circle(img2, refPoint, 2, (255,0,128), 2)
#------------------------------------------------------------


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
fv2 = extractFeature(img2, refPoint2,normalpoints2)


#------------Drawings for feature vector 2-------------------
cv2.line(img2,midLine[0],midLine[1],(255,0,128), 1)
cv2.line(img2,umax,lmax2,(0,0,255), 1)
cv2.circle(img2, lmax2, 2, (0,255,255), 2)
for x in points2:
    cv2.circle(img2, x, 2, (0,255,0), 2)

for point in normalpoints2:
    cv2.line(img2,point[0],point[1],(255,255,0), 1)
cv2.circle(img2, refPoint2, 2, (255,0,128), 2)
#------------------------------------------------------------

print(len(fv1),"->",fv1)
print(len(fv2),"->",fv2)

cv2.imshow('Original', img)
cv2.imshow('Painted', img2)
cv2.waitKey(0)
exit()





# x2 = int(((1/math.sqrt(1+m**2))*100 + x1))
# y2 = int(((m/math.sqrt(1+m**2))*100 + y1))
# cv2.line(img, (x1,y1),(x2,y2),(255),2)

# Feature Vector 1: (angle between reference line and line joining reference point and normal intersection point on the outer edge) 
# [-4.66, -2.54, -1.62, -1.17, -0.87, -0.65, -0.46, -0.31, -0.15, 0.0, 0.16, 0.33, 0.49, 0.67, 0.88, 1.13, 1.48, 2.06, 3.34]
# Feature Vector 2: (angle between reference line and line joining reference point and normal intersection point on the outer edge) 
# 9 -> [-3.97, -1.92, -1.08, -0.48, 0.0, 0.42, 0.88, 1.56, 3.15]