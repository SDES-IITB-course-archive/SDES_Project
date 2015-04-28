#!/usr/bin/env python

import cv2
import sys

class Video(object):
    def __init__(self):
        self.init=0

    def normal_exit(self):
        if(self.init==1):
            self.stop_video_capture()
        sys.exit()

    def catch_error(self,function,module,error):
        if(self.init==1):
            self.stop_video_capture()
        self.error_occurred_in(function,module)
        print error.message
        sys.exit()

    def error_occurred_in(self,function,module):
        print "The following error occurred in function",function,"from module",module

    def start_video_capture(self):
        try:
            self.video_handle=cv2.VideoCapture(0)
            self.init=1
        except cv2.error as cv2_error:
            self.catch_error("start_video_capture","video",cv2_error)

    def stop_video_capture(self):
        self.video_handle.release()
        cv2.destroyAllWindows()

    def get_next_frame(self):
        try:
            _,frame=self.video_handle.read()
            return frame
        except cv2.error as cv2_error:
            self.catch_error("get_next_frame","video",cv2_error)
