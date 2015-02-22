#!/usr/bin/python

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

def SnapSlide(inFile,cntFile,outFile):   
    Success=0
    # read input 
    print(inFile)
    img = cv2.imread(inFile)
    x0, y0, depth = img.shape
    print('Size of image is '+str(x0)+','+str(y0))
    # remove salt and pepper noise
    #img = cv2.bilateralFilter(img,20,100,100)
    # convert to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imwrite('gray.jpg',gray)
    small_area=True
    low_thr=150
    high_thr=200
    while small_area and low_thr<high_thr:
        # get edges
        edges = cv2.Canny(gray,low_thr,high_thr,apertureSize = 3)
        cv2.imwrite('edges.jpg',edges)
        #get hough lines
        lines = cv2.HoughLines(edges,1,np.pi/180,200)
        lines_img =np.zeros(edges.shape,dtype=edges.dtype)
        for rho,theta in lines[0]:
            draw_line(lines_img,rho,theta)
        cv2.imwrite('houghlines.jpg',lines_img)            
        edges=edges*lines_img
        t,edges= cv2.threshold(edges,0.1,255,cv2.THRESH_BINARY)
        
        kernel=np.ones((11,11),dtype='uint')
        edges = cv2.dilate(edges,kernel)
        t,edges= cv2.threshold(edges,0.1,255,cv2.THRESH_BINARY)
        cv2.imwrite('edges_lines.jpg',edges)
        # get contours
        contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        area_contour=[]
        for cnt in contours:
            area_contour.append(cv2.contourArea(cnt)/float(x0*y0))
            
        max_ind= area_contour.index(max(area_contour)) # get max area contour
        cv2.drawContours(img,contours,max_ind,(0,255,0),2)  
        print(contours[max_ind])
        hull = contours[max_ind]
        hull = cv2.convexHull(contours[max_ind])    # find the convex hull of         
        cv2.drawContours(img,[hull],0,(0,0,255),2)          
        if(area_contour[max_ind]<0.01):
            print('Couldnt find area larger than 1%, trying with reduced edge threshold')
            small_area=True
            low_thr-=10
            high_thr-=80
            continue
        else:
            small_area=False

        fraction=0
        while len(hull)!=4  and fraction<1:
            hull = cv2.approxPolyDP(hull,fraction*cv2.arcLength(hull,True),True)
            fraction+= 0.01
            
        if len(hull)==4:
            cv2.drawContours(img,[hull],0,(255,0,0),2)  
            src = np.float32([hull[0],hull[1],hull[2],hull[3]])
            dest = np.float32([[y0,0],[y0,x0],[0,x0],[0,0]])
            warp_mat = cv2.getPerspectiveTransform(src,dest)
            img_warped = cv2.warpPerspective(img,warp_mat,(y0,x0))
            cv2.imwrite(outFile,img_warped) 
            Success=1
    cv2.imwrite(cntFile,img)
    return Success
        
