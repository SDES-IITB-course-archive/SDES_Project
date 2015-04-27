#!/usr/bin/env python

import cv2
import numpy as np

def detect_pointer_in_rect(left_top_x,left_top_y,width,height):
    cap = cv2.VideoCapture(0)
    fgbg = cv2.BackgroundSubtractorMOG()
    while True:

        # Take each frame
        _, frame = cap.read()

        # Crop the frame according to the parameters specified
        frame_cropped = frame[left_top_x:left_top_x+height,left_top_y:left_top_y+width]

        # Convert BGR to HSV
        hsv_cropped = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2HSV)
#        print fgmask.shape
        print hsv_cropped.shape

#       This could be the other possible range
        #correct range
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

#        lower_blue = np.array([110,50,150])
#        upper_blue = np.array([130,255,255])

 #       lower_blue = np.array([120,70,10])
 #       upper_blue = np.array([255,250,50])

        #Threshold the HSV image to get only blue colors
#        mask_cropped = cv2.inRange(hsv_cropped, lower_blue, upper_blue)
        try:
            mask_cropped = cv2.inRange(hsv_cropped, lower_blue, upper_blue)
        except cv2.error as e:
            cap.release()
            cv2.destroyAllWindows()
            print e.message
            return e
            break

        # Bitwise-AND mask and original image
        res_cropped = cv2.bitwise_and(frame_cropped,frame_cropped, mask= mask_cropped)

        print fgbg.getMat(hsv_cropped)
        fgmask = fgbg.apply("abcd")

        cv2.imshow('frame_cropped',frame_cropped)
        cv2.imshow('mask_cropped',mask_cropped)
        cv2.imshow('res_cropped',res_cropped)
        cv2.imshow('fgmask',fgmask)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

if(__name__=="__main__"):
    left_top_x,left_top_y=100,100
    width,height=300,300
    detect_pointer_in_rect(left_top_x,left_top_y,width,height)

