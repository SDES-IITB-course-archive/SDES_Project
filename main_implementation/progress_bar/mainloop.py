import time
import sys
import numpy as np

import guigrid
from game import *
from video import *
from gui import *

def check_if_grid_size_fits_in_frame(grid,camframe,grid_position):
    camframe_width,camframe_height,_=camframe.shape
    if grid.width+grid_position[0]>camframe_width or grid.width+grid_position[1]>camframe_height:
       raise guigrid.SizeError("grid does not fit into webcam frame. Please \
       reduce grid size or gaps between dots.")
       sys.exit(1)
       
def get_text(player=None):
    text=""
    if player==None:
       if game_object.game_ended():
          winner=game_object.declare_winner()
          if winner!=None:
             text+="   Player "+winner+" won the game."
          else:
             text+="   It's a tie."
       else:
          owner_of_next_line=str(game_object.get_owner_of_next_line()+1)
          text+="    Next Player: "+owner_of_next_line
    
    elif player==1:
         player1boxes=str(game_object.no_of_boxes_of_players[0])
         text+= "Player 1: "+player1boxes
    elif player==2:
         player2boxes=str(game_object.no_of_boxes_of_players[1])
         text+= "Player 2: "+player2boxes
    return text 


def update_gui(camframe,grid,grid_position,pointer_location):
    camframe=cv2.flip(camframe,flipCode=1)
    camframe=blend_grid(camframe,grid.grid,grid_position)
    width,height,_=camframe.shape
    camframe=draw_next_player_color(camframe,width,height)
    camframe=write_text(camframe,width,height)
    cv2.imshow("Game_Window",camframe)
    cv2.waitKey(1)
    if user_wants_to_stop():
       webcam_video.stop_video_capture()
       sys.exit(1)

def blend_grid(camframe,grid,grid_position):
    if camframe==None or grid==None:
       return
    x,y=grid_position[0],grid_position[1]
    rows,cols,channels = grid.shape
    roi = camframe[x:x+rows, y:y+cols]
    gridgray = cv2.cvtColor(grid,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gridgray, 10, 255, cv2.THRESH_BINARY)
    mask_inverse = cv2.bitwise_not(mask)
    camframe_background = cv2.bitwise_and(roi,roi,mask = mask_inverse)
    grid_foreground = cv2.bitwise_and(grid,grid,mask = mask)
    grid_foreground= cv2.add(camframe_background,grid_foreground)
    blending=0.8
    dst = cv2.addWeighted(roi,1-blending,grid_foreground,blending,1)
    camframe[x:x+rows, y:y+cols ] = dst
    return camframe

def draw_pointer(camframe,pointer_location):
    radius=2
    color=(255,255,255)
    cv2.circle(camframe,(pointer_location[0],pointer_location[1]),radius,color,-1)
    return camframe


def draw_next_player_color(camframe,width,height):
    if game_object.get_owner_of_next_line()==0:
       deeper_color=make_deeper_color(colors[0])
    else:
       deeper_color=make_deeper_color(colors[1])
    
    cv2.circle(camframe,(50,50),10,deeper_color,-1)
    return camframe

def write_text(camframe,width,height):
   cv2.putText(camframe, get_text(1), (10,height-200), cv2.FONT_HERSHEY_PLAIN, 1.4, colors[0],thickness=2)
   cv2.putText(camframe, get_text(2), (170,height-200), cv2.FONT_HERSHEY_PLAIN, 1.4, colors[1],thickness=2)
   cv2.putText(camframe, get_text(), (310,height-200), cv2.FONT_HERSHEY_PLAIN, 1.4, (0,100,255),thickness=2)
   return camframe
   
def make_deeper_color(color):
    deeper_color=[0,0,0]
    for i in [0,1,2]:
        deeper_color[i]=int(color[i]*1.2)
        if deeper_color[i]>255:
           deeper_color[i]=255
    return tuple(deeper_color)

def convert_pointer_location(pointer_location,grid_position):
    pointer_location_inside_grid=(pointer_location[0]-grid_position[1],pointer_location[1]-grid_position[0])
    return pointer_location_inside_grid

def get_system_time():
    return time.time()

def line_already_selected(line):
    if (line_to_dot_list(line) in game_object.list_of_lines_drawn):
        return True
    else:
        return False

def create_grid(row,col,dot_radius=8,dots_gap=60,dottype=1,color=(46,266,250),fatigue=None,player1_boxcolor=None,player2_boxcolor=None):
    new_grid=guigrid.GuiGrid(row,col,dot_radius,dots_gap,dottype,color,fatigue,player1_boxcolor,player2_boxcolor)
    return new_grid

def initiate_game_states(row,col,number_of_players):
    game_object=Game([row,col],number_of_players)
    return game_object

def initiate_webcam():
    webcam_video=Video()
    try:
        webcam_video.start_video_capture()
    except cv2.error as cv2_error:
        webcam_video.catch_error("initiate_webcam","mainloop","cv2_error")
    return webcam_video

def initiate_pointer(color,pointer_window=None):
    mypointer=Pointer(color,pointer_window)
    return mypointer

def initial_set_up(webcam_video,pointers):
    try:
        print "First calibrate the pointer for player 1"
        pointers[0].calibrate_pointer(webcam_video)
        print "First calibrate the pointer for player 2"
        pointers[1].calibrate_pointer(webcam_video)
        print "Thanks, you can now start playing"
        return webcam_video,pointers
    except cv2.error as cv2_error:
        webcam_video.catch_error("initial_set_up","mainloop","cv2_error")

def convert_dot_to_tuple(dot):
    return (dot.get_x(),dot.get_y())

def draw_boxes(boxes,player_number):
    box_formed_0=boxes[0]
    if box_formed_0!=None:
       left_top_dot_of_box_0=convert_dot_to_tuple(box_formed_0[0][0])
       grid.draw_box(left_top_dot_of_box_0,player_number)
    box_formed_1=boxes[1]
    if box_formed_1!=None:
       left_top_dot_of_box_1=convert_dot_to_tuple(box_formed_1[0][0])
       grid.draw_box(left_top_dot_of_box_1,player_number)

def line_to_dot_list(line):
    return [Dot(line[0]),Dot(line[1])]

def game_logic(selected_line):
    game_in_progress=True
    line_in_form_of_dots=[Dot(selected_line[0]),Dot(selected_line[1])]
    game_object.update_list_of_drawn_lines_with(line_in_form_of_dots)
    
    box_formed,boxes=game_object.box_formed_by(line_in_form_of_dots)
    game_object.set_owner_of_next_line(box_formed)
    if box_formed:
       owner_of_the_box=game_object.get_owner_of_last_line()
       draw_boxes(boxes,owner_of_the_box)   
       game_object.update_no_of_boxes_of_players(owner_of_the_box,boxes)
       if(game_object.game_ended()):
             game_in_progress =False            
    return game_in_progress
    

row,col=3,2
dot_radius,dots_gap,dottype,color=6,60,1,(46,266,250)
max_allowed_pointer_miss=3
number_of_players=2
grid_position=(100,100)
colors=[(0,0,255),(110,210,10)]
total_global_waiting_time=1.0
    
grid=create_grid(row,col,dot_radius,dots_gap,dottype,color,fatigue=4,
                 player1_boxcolor=colors[0],player2_boxcolor=colors[1])
game_object=initiate_game_states(row,col,number_of_players)
webcam_video=initiate_webcam()
pointers=[initiate_pointer(colors[0],[92,128,96,236,0,288]),
          initiate_pointer(colors[1],[37,71,118,216,49,188])
         ]
check_if_grid_size_fits_in_frame(grid,webcam_video.get_next_frame(),grid_position)
webcam_video,pointers=initial_set_up(webcam_video,pointers)
cv2.namedWindow("Game_Window",cv2.WINDOW_NORMAL)

def main():
	game_in_progress=True
	player=0
	while True:
	      total_waiting_time=total_global_waiting_time
	      frame=webcam_video.get_next_frame()
	      player=game_object.get_owner_of_next_line()
	      _,pointer_location=pointers[player].detect_pointer(frame)
	      if pointer_location==None:
		 update_gui(frame,grid,grid_position,pointer_location=None)
		 continue
	      pointer_location_inside_grid=convert_pointer_location(pointer_location,grid_position)
	      selected_line=grid.find_selected_line(pointer_location_inside_grid)
	      
	      if selected_line==None or line_already_selected(selected_line):
		 update_gui(frame,grid,grid_position,pointer_location)
		 continue
		 
	      start_time=get_system_time()
	      delay=0
	      pointer_miss=0
	      progress_bar_drawn=False
	      while delay<=total_waiting_time:
		    frame=webcam_video.get_next_frame()
		    player=game_object.get_owner_of_next_line()
		    _,pointer_location=pointers[player].detect_pointer(frame)
		    if pointer_location==None:
		       total_waiting_time=total_waiting_time*1.1
		       pointer_miss+=1
		       if pointer_miss>max_allowed_pointer_miss:
		          break;
		       update_gui(frame,grid,grid_position,pointer_location=None)
		       continue
		    pointer_location_inside_grid=convert_pointer_location(pointer_location,grid_position)
		    new_selected_line=grid.find_selected_line(pointer_location_inside_grid)
		    if new_selected_line==selected_line:
		       grid.draw_progressbar_over_last_selected_line(delay/total_waiting_time)
		       progress_bar_drawn=True
		       delay=get_system_time()-start_time
		       update_gui(frame,grid,grid_position,pointer_location)
		       continue
		    else:
		       update_gui(frame,grid,grid_position,pointer_location) 
		       break
	      if delay>total_waiting_time:
		 grid.draw_last_selected_line()
		 progress_bar_drawn=False
		 game_in_progress=game_logic(selected_line)
		 update_gui(frame,grid,grid_position,pointer_location)
	      if progress_bar_drawn==True:
		 grid.remove_progress_bar()
	      if game_in_progress==False and user_wants_to_stop():
		 webcam_video.stop_video_capture()
		 break

if __name__=="__main__":
   main()

