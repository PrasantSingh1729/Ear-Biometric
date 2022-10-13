import cv2
screen="Drawing"
img=cv2.imread("img/001_.jpg")
cv2.namedWindow(screen)
eraser=False 
radius = 20

def draw_circle(x,y):
        # 'erase' circle
        cv2.circle(img, ( x, y), radius, (0, 0, 0), -1)
        cv2.imshow(screen,img)

def handleMouseEvent(event,x,y,flags,param):
      global eraser , radius     
      if (event==cv2.EVENT_MOUSEMOVE):
              # update eraser position
            if eraser==True:
                  draw_circle(x,y)
      elif (event==cv2.EVENT_MOUSEWHEEL):
              # change eraser radius
            if flags > 0:
                radius +=   5
            else:
                    # prevent issues with < 0
                if radius > 10:
                    radius -=   5
      elif event == cv2.EVENT_LBUTTONUP:
              # stop erasing
            eraser = False
      elif (event==cv2.EVENT_LBUTTONDOWN):
              # start erasing
            eraser=True
            draw_circle(x,y)


cv2.setMouseCallback(screen,handleMouseEvent)
# show initial image
cv2.imshow(screen,img)
cv2.waitKey(0)
cv2.destroyAllWindows()