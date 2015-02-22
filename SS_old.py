#!/usr/bin/python

import cv2
import sys
import numpy as np

def GetOptimalDepth(img,p1,p2,axis,xstar):
    outval=np.std(img) 
    diffval=[]

    for d in range(10,int(xstar[axis])+1):
        x1=xstar[axis]-d
        x2=xstar[axis]
        if axis==0:
            inval=np.std(img[x1:x2,p1:p2])
        if axis==1:
            inval=np.std(img[p1:p2,x1:x2])
        if outval<inval or x1==0:
            x1opt=x1
            break

    for d in range(10,int(img.shape[axis]-xstar[axis])+1):
        x2=xstar[axis]+d
        #print(x2)
        if axis==0:
            inval=np.std(img[x1:x2,p1:p2])
        if axis==1:
            inval=np.std(img[p1:p2,x1:x2])
        if(outval<inval or x2==img.shape[axis]):
            print('here')
            x2opt=x2
            break
            
    return x1opt,x2opt


def SnapSlide(inFile,outFile,xstar):   
    Success=0
    # read input 
    print(inFile)
    img = cv2.imread(inFile)
    x0, y0, depth = img.shape
    print('Size of image is '+str(x0)+','+str(y0))
    
    y1=xstar[1]-1
    y2=xstar[1]+1
    x1,x2=GetOptimalDepth(img,y1,y2,0,xstar)
    for ii in range(1):
        if ii%2 == 0:
            y1,y2=GetOptimalDepth(img,x1,x2,1,xstar)
        else:
            x1,x2=GetOptimalDepth(img,y1,y2,0,xstar)
        print(x1,x2,y1,y2)            
        
    cv2.line(img,(int(x1),int(y1)),(int(x1),int(y2)),(0,0,255),2)
    cv2.line(img,(int(x1),int(y2)),(int(x2),int(y2)),(0,0,255),2)
    cv2.line(img,(int(x2),int(y2)),(int(x2),int(y1)),(0,0,255),2)
    cv2.line(img,(int(x2),int(y1)),(int(x1),int(y1)),(0,0,255),2)
    cv2.imwrite('square.jpg',img)
    return Success
        
if __name__ == '__main__': 
    SnapSlide(sys.argv[1],sys.argv[2],[float(sys.argv[3]),float(sys.argv[4])])        
