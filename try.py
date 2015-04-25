#!/usr/bin/env python

import cv2
import numpy as np

# Roughly the values are : LowH = 107, HighH = 111
#                          LowS = 151, HighS = 255
#                          LowV = 43,  HighV = 255

def nothing(x):
    pass

def detect_pointer_in_rect():
    try:
        iLowH=0
        iHighH=179
        iLowS=0
        iHighS=255
        iLowV=0
        iHighV=255
        cv2.namedWindow('Control')
        cv2.createTrackbar('LowH','Control',0,179,nothing)
        cv2.createTrackbar('HighH','Control',0,179,nothing)
        cv2.createTrackbar('LowS','Control',0,255,nothing)
        cv2.createTrackbar('HighS','Control',0,255,nothing)
        cv2.createTrackbar('LowV','Control',0,255,nothing)            
        cv2.createTrackbar('HighV','Control',0,255,nothing)    
        
        cap = cv2.VideoCapture(0)
        while True:

            # Take each frame
            _, imgOriginal = cap.read()
            
            # Convert BGR to HSV
            imgHSV=cv2.cvtColor(imgOriginal,cv2.COLOR_BGR2HSV)
            
            iLowH = cv2.getTrackbarPos('LowH','Control')
            iLowS = cv2.getTrackbarPos('LowS','Control')
            iLowV = cv2.getTrackbarPos('LowV','Control')
            iHighH = cv2.getTrackbarPos('HighH','Control')
            iHighS = cv2.getTrackbarPos('HighS','Control')            
            iHighV = cv2.getTrackbarPos('HighV','Control')            
            
            imgThresholded=cv2.inRange(imgHSV,np.array([iLowH,iLowS,iLowV]),np.array([iHighH,iHighS,iHighV]))
            
#            cv2.imshow("inRange",imgThresholded)
            imgThresholded=cv2.erode(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
            
            imgThresholded=cv2.dilate(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))        
            
            imgThresholded=cv2.dilate(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
            imgThresholded=cv2.erode(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
            
            cv2.imshow("Thresholded image",imgThresholded)
            cv2.imshow("Original",imgOriginal)
            
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                cap.release()
                cv2.destroyAllWindows()
                break
    except cv2.error as e:
        print e.message
        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    detect_pointer_in_rect()
