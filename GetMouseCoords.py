import cv2

class mousecoords:
    def __init__(self):
        self.x = -1
        self.y = -1
    
    def getcoords(self,event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDBLCLK:      # here event is left mouse button double-clicked
            print(x,y)
            self.x = x
            self.y = y
        
    def returncoords(self):
        return self.x, self.y
                


def GetMouseCoords(img):
    cv2.namedWindow("contours",0)
    x0, y0, depth = img.shape
    cv2.resizeWindow("contours", x0/5,y0/5)
    interior_pt = mousecoords()
    cv2.setMouseCallback("contours",interior_pt.getcoords,img)
    cv2.imshow("contours",img)
    while(1):
        if cv2.waitKey(20) & 0xFF == 27:
            break
    
    intx,inty = interior_pt.returncoords()
    
    if intx <= x0 and inty<= y0:
        cv2.destroyAllWindows()
    return intx, inty
