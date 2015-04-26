#!/usr/bin/env python

from game import *
from grid import *
from video import *
from gui import *

def main():
    grid_size_in_dots=[10,10]
    grid_size_in_pixels=[200,200]
    no_of_players=2
    left_top=[100,100]
    dot_size=3
    
    mygame=Game(grid_size,no_of_players)
    new_grid=Grid(left_top,grid_size_in_dots,grid_size_in_pixels,dot_size)
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
        except cv2.error as cv2_error:
            webcam_video.catch_error("main","main","cv2_error")
        new_grid.draw_grid_on(latest_frame)
        
        try:
            my_input,frame_with_pointer_located=mypointer.received_input(latest_frame,new_grid)
            cv2.imshow("Game_window",frame_with_pointer_located)
        except cv2.error as cv2_error:
            webcam_video.catch_error("received_input","gui",cv2_error)
        if(my_input==None):
            continue
        
        else:
            latest_line=my_input
            if(latest_line in mygame.list_of_lines_drawn):
                print "This line is already drawn. Choose another."
                continue
            new_grid.draw_line(latest_line)
            mygame.update_list_of_drawn_lines_with(latest_line)
            box_formed,box=mygame.box_formed_by(latest_line)
            mygame.set_owner_of_next_line(box_formed)
            if(box_formed):
                owner_of_the_box=mygame.get_owner_of_last_line()
                new_grid.fill_box(box,owner_of_the_box)
                mygame.update_no_of_boxes_of_players(owner_of_the_box)
                if(mygame.game_ended()):
                    print "The entire grid is filled"
                    mygame.declare_winner()
                    if(user_wants_to_stop()):
                        webcam_video.stop_video_capture()
                        print "Thanks for playing!"
                    break

if(__name__=="__main__"):
    main()
