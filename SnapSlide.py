#!/usr/bin/python

import os, sys
from SnapSlideArgs import getArgs
from GetMouseCoords import GetMouseCoords
import cv2
import numpy as np



## draw line of given rho and theta on image
def draw_line(img,rho,theta):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 10000*(-b))
    y1 = int(y0 + 10000*(a))
    x2 = int(x0 - 10000*(-b))
    y2 = int(y0 - 10000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(255),10)
    return img

def SnapSlide(inFile,outFile,verbose): 
    Success=0
    orig = cv2.imread(inFile)
    img = orig.copy()
    x0, y0, depth = img.shape
    if verbose==1:
        print('Size of image is '+str(x0)+','+str(y0))
    # convert to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    small_area=True
    low_thr=150
    high_thr=200
    
    edges = cv2.Canny(gray,low_thr,high_thr,apertureSize = 3)
    
    # get contours
    contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        hull = cv2.convexHull(cnt)    # find the convex hull of         
        cv2.drawContours(img,[hull],0,(0,0,255),2)   
        
    inty,intx = GetMouseCoords(img)
    print(intx,inty)
    
    eligible_cnts=[]       
    for e,cnt in enumerate(contours):
        dist = cv2.pointPolygonTest(cnt,(inty,intx),True)
        if dist>0:
            eligible_cnts.append(e)
    print(eligible_cnts)
    
    hull = cv2.convexHull(contours[eligible_cnts[0]]) 
    fraction=0.1
    while len(hull)!=4  and fraction<1:
        hull = cv2.approxPolyDP(hull,fraction*cv2.arcLength(hull,True),True)
        fraction+= 0.01
            
    if len(hull)==4:
        src = np.float32([hull[0],hull[1],hull[2],hull[3]])
        dest = np.float32([[y0,0],[y0,x0],[0,x0],[0,0]])
        warp_mat = cv2.getPerspectiveTransform(src,dest)
        img_warped = cv2.warpPerspective(orig,warp_mat,(y0,x0))
        cv2.imwrite(outFile,img_warped) 
        Success=1
      
    return Success
        
if __name__ == '__main__': 
    inFile,outFile,verbose=getArgs(sys.argv[1:])
    retval=SnapSlide(inFile,outFile,verbose)
    if retval==1:
        print('Snapped slide!')
    
    
