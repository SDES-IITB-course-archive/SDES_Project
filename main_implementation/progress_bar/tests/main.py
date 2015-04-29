#!/usr/bin/env python

import numpy as np

from game import *
import grid
from video import *
from gui import *

def main():
    rows=5
    cols=5
    no_of_players=2
    mygame=Game([rows,cols],no_of_players)
    new_grid=grid.Grid(row=rows,col=cols,dotRadius=8,dotsGap=60,dottype=1,color=(46,266,250))
    webcam_video=Video()
    mypointer=Pointer()
    try:
        webcam_video.start_video_capture()
        print "First calibrate the pointer"
        mypointer.calibrate_pointer(webcam_video)
        print "Thanks, you can now start playing"
    except cv2.error as cv2_error:
        webcam_video.catch_error("main","main","cv2_error")

    while True:
        try:
            latest_frame=webcam_video.get_next_frame()
            k=cv2.waitKey(10)
            cv2.namedWindow("Game_window",cv2.WINDOW_NORMAL)
            m=cv2.waitKey(5)
            grid_image=new_grid.draw_grid(latest_frame)
            another_frame=new_grid.blendGrid(latest_frame,0,0)
            cv2.imshow("Game_window",another_frame)
        except cv2.error as cv2_error:
            webcam_video.catch_error("main","main","cv2_error")

        try:
            my_input,frame_with_pointer_located=mypointer.received_input(webcam_video,new_grid)
        except cv2.error as cv2_error:
            webcam_video.catch_error("received_input","gui",cv2_error)
        if(my_input==None):
            cv2.imshow("Game_window",frame_with_pointer_located)
            continue

        else:
            cv2.imshow("Game_window",frame_with_pointer_located)
            latest_line=my_input
            if(latest_line in mygame.list_of_lines_drawn):
                print "This line is already drawn. Choose another."
                continue
            new_grid.drawLine(latest_line)
            mygame.update_list_of_drawn_lines_with(latest_line)
            box_formed,boxes=mygame.box_formed_by(latest_line)
            mygame.set_owner_of_next_line(box_formed)
            if(box_formed):
                owner_of_the_box=mygame.get_owner_of_last_line()
                if(boxes[0]!=None):
                    new_grid.drawBox([boxes[0][0][0].get_x(),boxes[0][0][0].get_y()],owner_of_the_box)
                if(boxes[1]!=None):
                    new_grid.drawBox([boxes[1][0][0].get_x(),boxes[1][0][0].get_y()],owner_of_the_box)
                mygame.update_no_of_boxes_of_players(owner_of_the_box,boxes)
                if(mygame.game_ended()):
                    print "The entire grid is filled"
                    mygame.declare_winner()
                    if(user_wants_to_stop()):
                        webcam_video.stop_video_capture()
                        print "Thanks for playing!"
                    break

if(__name__=="__main__"):
    main()
