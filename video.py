#!/usr/bin/env python

import cv2
from errorhandling import *

class Video(object):
    def __init__(self):
        self.init=0

    def catch_error(function,module,error):
        if(self.init==1):
            stop_video_capture(cap)
        error_occurred_in(function,module)
        print cv2_error.message
        exit()

    def error_occurred_in(function,module):
        print "The following error occurred in function",function,"from module",module

    def start_video_capture(self):
        try:
            self.video_handle=cv2.VideoCapture(0)
            self.init=1
        except cv2.error as cv2_error:
            self.catch_error("start_video_capture","video",cv2_error)

    def wait(self,delay):
        pass

    def stop_video_capture(self):
        self.video_handle.release()
        cv2.destroyAllWindows()

    def get_next_frame(self):
        try:
            _,frame=self.video_handle.read()
            return frame
        except cv2.error as cv2_error:
            self.catch_error("get_next_frame","video",cv2_error)
