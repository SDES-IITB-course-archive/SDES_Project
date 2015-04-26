#!/usr/bin/env python

import cv2
import numpy as np
from video import *
import sys

class Pointer(object):
    def __init__(self):
        self.calibrated=0
        self.pointer_window=[0,0,0,0,0,0]


    def received_input(self,latest_frame,new_grid):
        if self.calibrated:
            frame,position_of_pointer=self.detect_pointer(latest_frame)
            if position_of_pointer==None:
                return None
            if(new_grid.out_of_grid(position_of_pointer)):
                return None
            else:
                initial_line=self.get_line_selected_by_pointer(new_grid,position_of_pointer)
                counter=0
                while(counter<max_count):
                    wait(delay)
                    frame,position_of_pointer=self.detect_pointer(latest_frame)
                    if(new_grid.out_of_grid(position_of_pointer)):
                        return None
                    else:
                        final_line=self.get_line_selected_by_pointer()
                        if(initial_line[0]!=final_line[0] and initial_line[1]!=final_line[1]):
                            return None,frame
                return initial_line,frame
        else:
            print "please, calibrate the pointer first."
            sys.exit()

    def detect_pointer(self,frame):
        if self.calibrated:
            [lower_hue,upper_hue,lower_sat,upper_sat,lower_value,upper_value]=self.pointer_window
        else:
            print "please, calibrate the pointer first."
            sys.exit()
        stamp=self.detect_and_stamp_the_pointer_in(frame)
        if stamp==None:
            return
        thresholded,frame_with_pointer_detected,[centroid_x,centroid_y]=stamp
        return frame,[centroid_x,centroid_y]

    def _open_image(self,thresholded):
        thresholded=cv2.erode(thresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
        thresholded=cv2.dilate(thresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
        return thresholded

    def _close_image(self,thresholded):
        thresholded=cv2.dilate(thresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
        thresholded=cv2.erode(thresholded,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
        return thresholded

    def _mask(self,hsv):
        [lower_hue,upper_hue,lower_sat,upper_sat,lower_value,upper_value]=self.pointer_window

        thresholded=cv2.inRange(hsv,np.array([lower_hue,lower_sat,lower_value]),np.array([upper_hue,upper_sat,upper_value]))
        thresholded=self._open_image(thresholded)
        thresholded=self._close_image(thresholded)

        return thresholded

    def detect_and_stamp_the_pointer_in(self,frame):
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        thresholded=self._mask(hsv)
        
        mom=cv2.moments(thresholded)
        try:
            centroid_x=int(mom['m10']/mom['m00'])
            centroid_y=int(mom['m01']/mom['m00'])
            cv2.circle(frame,(centroid_x,centroid_y),5,(255,255,255),-1)
            cv2.circle(thresholded,(centroid_x,centroid_y),3,(0,0,0),-1)
            return thresholded,frame,[centroid_x,centroid_y]
        except ZeroDivisionError as z:
            pass
            
        
    def calibrate_pointer(self,webcam_video):
        def nothing(trackbar_position):
            pass
        try:

            cv2.namedWindow('Control')

            try:
                cv2.createTrackbar('LowH','Control',0,179,nothing)
                cv2.createTrackbar('HighH','Control',0,179,nothing)
                cv2.createTrackbar('LowS','Control',0,255,nothing)
                cv2.createTrackbar('HighS','Control',0,255,nothing)
                cv2.createTrackbar('LowV','Control',0,255,nothing)
                cv2.createTrackbar('HighV','Control',0,255,nothing)
            except TypeError as te:
                print "caught typeerror"

            cv2.setTrackbarPos('LowH','Control',0)
            cv2.setTrackbarPos('HighH','Control',179)
            cv2.setTrackbarPos('LowS','Control',0)
            cv2.setTrackbarPos('HighS','Control',255)
            cv2.setTrackbarPos('LowV','Control',0)
            cv2.setTrackbarPos('HighV','Control',255)

            while True:
                frame=webcam_video.get_next_frame()

                lower_hue = cv2.getTrackbarPos('LowH','Control')
                lower_sat = cv2.getTrackbarPos('LowS','Control')
                lower_value = cv2.getTrackbarPos('LowV','Control')
                upper_hue = cv2.getTrackbarPos('HighH','Control')
                upper_sat = cv2.getTrackbarPos('HighS','Control')
                upper_value = cv2.getTrackbarPos('HighV','Control')

                self.pointer_window=[lower_hue,upper_hue,lower_sat,upper_sat,lower_value,upper_value]

                stamp=self.detect_and_stamp_the_pointer_in(frame)
                if stamp==None:
                    continue
                thresholded,frame_with_pointer_detected,[centroid_x,centroid_y]=stamp
                cv2.imshow("Calibration",thresholded)
                cv2.imshow("Detected_pointer",frame_with_pointer_detected)

                if user_wants_to_stop():
                    cv2.destroyWindow("Detected_pointer")
                    cv2.destroyWindow("Control")
                    cv2.destroyWindow("Calibration")
                    if __name__=="__main__":
                        webcam_video.normal_exit()
                    self.calibrated=1
        except cv2.error as cv2_error:
            webcam_video.catch_error("calibrate_pointer","gui",cv2_error)

    def get_line_selected_by_pointer(self,new_grid,position_of_pointer):
        
        pass

def user_wants_to_stop():
    while True:
        k=cv2.waitKey(5) & 0xFF
        if(k==27):
            return True
        break

if __name__=="__main__":
    webcam_video=Video()
    webcam_video.start_video_capture()
    mypointer=Pointer()
    mypointer.calibrate_pointer(webcam_video)
