import game
import grid

def main():
    while True;
        frame=capture_frame()
        new_grid=grid(left_top_x,left_top_y,height,width)
        gridded_frame=new_grid.draw_on(frame)
        if(pointer_detected(gridded_frame)):
            if(pointer_within_grid(gridded_frame)):
                if(gesture_made()):




        else:



if(__name__=="__main__"):
    main()
