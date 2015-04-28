#!/usr/bin/env python

import cv2
import numpy as np
from video import *
import sys
from dot import *

class Pointer(object):
    def __init__(self,color,pointer_window=None):
        self.calibrated=0
        if pointer_window==None:
           self.pointer_window=[0,179,0,255,0,255]
        else:
           self.pointer_window=pointer_window
        self.color=color

    def received_input(self,webcam_video,new_grid):
        if self.calibrated:
            latest_frame=webcam_video.get_next_frame()
            frame_with_pointer_detected,position_of_pointer=self.detect_pointer(latest_frame)
            frame_with_pointer_detected=new_grid.blendGrid(frame_with_pointer_detected,0,0)
            if position_of_pointer==None:
                return None,frame_with_pointer_detected
            if(new_grid.isOutsideArea(position_of_pointer[0],position_of_pointer[1])):
                return None,frame_with_pointer_detected
            else:
                initial_line=new_grid.findSelectedLine(position_of_pointer[0],position_of_pointer[1])
                if initial_line==None:
                    return None,frame_with_pointer_detected
                counter=0
                total_delay=20
                for i in xrange(0,total_delay/2):
                    latest_frame=webcam_video.get_next_frame()
                    cv2.waitKey(2)
                    frame_with_pointer_detected,position_of_pointer=self.detect_pointer(latest_frame)
                    frame_with_pointer_detected=new_grid.blendGrid(frame_with_pointer_detected,0,0)
                    if position_of_pointer==None:
                        cv2.imshow("Game_window",frame_with_pointer_detected)
                        continue
                    if(new_grid.isOutsideArea(position_of_pointer[0],position_of_pointer[1])):
                        cv2.imshow("Game_window",frame_with_pointer_detected)
                        continue
                    else:
                        final_line=new_grid.findSelectedLine(position_of_pointer[0],position_of_pointer[1])
                        if final_line==None:
                            cv2.imshow("Game_window",frame_with_pointer_detected)
                            continue
                        if(initial_line[0]!=final_line[0] and initial_line[1]!=final_line[1]):
                            cv2.imshow("Game_window",frame_with_pointer_detected)
                            continue
                        if counter==7:
                            return [Dot(initial_line[0]),Dot(initial_line[1])],frame_with_pointer_detected
                        else:
                            counter+=1
                return None,frame_with_pointer_detected
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
        if stamp[2]==None:
            return frame,None
        thresholded,frame_with_pointer_detected,[centroid_x,centroid_y]=stamp
        [nrows,ncols,_]=frame_with_pointer_detected.shape
        return frame_with_pointer_detected,[ncols-centroid_x,centroid_y]

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
            cv2.circle(frame,(centroid_x,centroid_y),5,self.color,-1)
            cv2.circle(thresholded,(centroid_x,centroid_y),3,self.color,-1)
            return thresholded,frame,[centroid_x,centroid_y]
        except ZeroDivisionError as z:
            return thresholded,frame,None

    def calibrate_pointer(self,webcam_video):
        def nothing(trackbar_position):
            pass
        try:
            cv2.namedWindow('Control')

            cv2.createTrackbar('LowH','Control',0,179,nothing)
            cv2.createTrackbar('HighH','Control',0,179,nothing)
            cv2.createTrackbar('LowS','Control',0,255,nothing)
            cv2.createTrackbar('HighS','Control',0,255,nothing)
            cv2.createTrackbar('LowV','Control',0,255,nothing)
            cv2.createTrackbar('HighV','Control',0,255,nothing)

            [lower_hue,upper_hue,lower_sat,upper_sat,lower_value,upper_value]=self.pointer_window

            cv2.setTrackbarPos('LowH','Control',lower_hue)
            cv2.setTrackbarPos('HighH','Control',upper_hue)
            cv2.setTrackbarPos('LowS','Control',lower_sat)
            cv2.setTrackbarPos('HighS','Control',upper_sat)
            cv2.setTrackbarPos('LowV','Control',lower_value)
            cv2.setTrackbarPos('HighV','Control',upper_value)

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
                
                if(stamp[2]==None):
                    cv2.imshow("Detected_pointer",stamp[1])
                    cv2.waitKey(5)
                    cv2.imshow("Calibration",stamp[0])
                    cv2.waitKey(5)
                    if user_wants_to_stop():
                        cv2.destroyWindow("Detected_pointer")
                        cv2.waitKey(4)
                        cv2.destroyWindow("Control")
                        cv2.waitKey(4)
                        cv2.destroyWindow("Calibration")
                        cv2.waitKey(4)
                        if __name__=="__main__":
                            webcam_video.normal_exit()
                        self.calibrated=1
                        return
                    continue

                thresholded,frame_with_pointer_detected,[centroid_x,centroid_y]=stamp
                cv2.imshow("Calibration",thresholded)
                cv2.waitKey(1)
                cv2.imshow("Detected_pointer",frame_with_pointer_detected)
                cv2.waitKey(1)

                if user_wants_to_stop():
                    cv2.destroyWindow("Detected_pointer")
                    cv2.waitKey(4)
                    cv2.destroyWindow("Control")
                    cv2.waitKey(4)
                    cv2.destroyWindow("Calibration")
                    cv2.waitKey(4)
                    if __name__=="__main__":
                        webcam_video.normal_exit()
                    self.calibrated=1
                    return
        except cv2.error as cv2_error:
            webcam_video.catch_error("calibrate_pointer","gui",cv2_error)

def user_wants_to_stop():
    k=cv2.waitKey(10) & 0xFF
    return k==27

if __name__=="__main__":
    webcam_video=Video()
    webcam_video.start_video_capture()
    mypointer=Pointer()
    mypointer.calibrate_pointer(webcam_video)
