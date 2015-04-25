#!/usr/bin/env python

def catch_error(function,module,error):
    stop_video_capture(cap)
    error_occurred_in(function,module)
    print cv2_error.message
    exit()

def error_occurred_in(function,module):
    print "The following error occurred in function",function,"from module",module
