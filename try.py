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

#        For keychain in my room at night
#        cv2.setTrackbarPos('LowH','Control',91)
#        cv2.setTrackbarPos('HighH','Control',114)
#        cv2.setTrackbarPos('LowS','Control',151)
#        cv2.setTrackbarPos('HighS','Control',255)
#        cv2.setTrackbarPos('LowV','Control',43)
#        cv2.setTrackbarPos('HighV','Control',255)

#        For Tanmoy's pen in his room at night
        cv2.setTrackbarPos('LowH','Control',85)
        cv2.setTrackbarPos('HighH','Control',125)
        cv2.setTrackbarPos('LowS','Control',177)
        cv2.setTrackbarPos('HighS','Control',255)
        cv2.setTrackbarPos('LowV','Control',13)
        cv2.setTrackbarPos('HighV','Control',97)

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

            imgThresholded=cv2.erode(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
            imgThresholded=cv2.dilate(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

            imgThresholded=cv2.dilate(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
            imgThresholded=cv2.erode(imgThresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

            cv2.imshow("Thresholded image",imgThresholded)
#            print imgThresholded

#            image,contours=cv2.findContours(imgThresholded,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#            try:
#                imgContours=cv2.drawContours(imgThresholded,contours,1,(0,255,0),3)
#                cv2.imshow("Contours",imgContours)
#            except (TypeError,cv2.error):
#                pass

            mom=cv2.moments(imgThresholded)
            try:
                centroid_x=int(mom['m10']/mom['m00'])
                centroid_y=int(mom['m01']/mom['m00'])
                cv2.circle(imgThresholded,(centroid_x,centroid_y),3,(0,0,0),-1)
                cv2.circle(imgOriginal,(centroid_x,centroid_y),5,(255,255,255),-1)
            except ZeroDivisionError as z:
                pass

            cv2.imshow("Original",imgOriginal)
            cv2.imshow('Detected_centroids',imgThresholded)

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
