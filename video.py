#!/usr/bin/env python

import cv2
from errorhandling import *

class Video(object):
    def __init__(self):
        try:
            self.video_handle=cv2.VideoCapture(0)
            
        except cv2.error as cv2_error:
            self.catch_error("start_video_capture","video",cv2_error)

    def wait(self,delay):
        pass

    def stop_video_capture(self):
        video_handle.release()
        cv2.destroyAllWindows()

    def get_next_frame(self,):
        try:
            _,frame=cap.read()
            return frame
        except cv2.error as cv2_error:
            catch_error("get_next_frame","video",cv2_error)
