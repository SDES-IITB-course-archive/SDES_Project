import time
import grid

import numpy as np

from game import *
from video import *
from gui import *

row,col=6,6
max_allowed_pointer_miss=3
number_of_players=2
grid_position=(10,12)

def updateGUI(camframe,grid,grid_position,pointer_location):
    camframe=blendGrid(camframe,grid.grid,grid_position)
    if pointer_location!=None:
       drawPointer(camframe,pointer_location)
    cv2.waitKey(5)
    cv2.imshow("Game_Window",camframe)
    cv2.waitKey(5)

def blendGrid(camframe,grid,grid_position):
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

def drawPointer(camframe,pointer_location):
    radius=2
    color=(255,255,255)
    cv2.circle(camframe,(pointer_location[0],pointer_location[1]),radius,color,-1)
    return camframe

def convert_pointer_location(pointer_location,grid_position):
    pointer_location_inside_grid=(pointer_location[0]-grid_position[0],pointer_location[1]-grid_position[1])
    return pointer_location_inside_grid

def get_system_time():
    return time.time()

def line_already_selected(line):
    if (line in game_object.list_of_lines_drawn):
        return True

def create_grid(row,col,dotRadius=8,dotsGap=60,dottype=1,color=(46,266,250)):
    new_grid=grid.Grid(row,col,dotRadius,dotsGap,dottype,color)
    return new_grid

def initiate_game_states(row,col,number_of_players):
    game_object=Game([row,col],number_of_players)
    return game_object

def initiate_webcam():
    webcam_video=Video()
    return webcam_video

def initiate_pointer():
    mypointer=Pointer()
    return mypointer

def initial_set_up(webcam_video,pointer):
    try:
        webcam_video.start_video_capture()
        print "First calibrate the pointer"
        pointer.calibrate_pointer(webcam_video)
        print "Thanks, you can now start playing"
        return webcam_video,pointer
    except cv2.error as cv2_error:
        webcam_video.catch_error("initial_set_up","mainloop","cv2_error")

def game_logic(selected_line,player_number):
    game_object.update_list_of_drawn_lines_with(selected_line)
    winning_status=0
    if game_object.boxFormed(selected_line,player_number):
       left_top_dot_of_box=game_object.get_last_box_formed()
       grid.drawBox(left_top_dot_of_box,player_number)
       if game_object.game_ended():
          return game_object.get_winning_status()
          #it returns winning_status,winning_player,winning_number,total_number
       else:
          next_player=(player_number+1)%number_of_players
          return winning_status, next_player, None, None
    return winning_status, player_number, None , None

grid=create_grid(row,col,dotRadius=8,dotsGap=60,dottype=1,color=(46,266,250))
game_object=initiate_game_states(row,col,number_of_players)
webcam_video=initiate_webcam()
pointer=initiate_pointer()
webcam_video,pointer=initial_set_up(webcam_video,pointer)

winning_status=0
player=0
while winning_status==0:
      total_waiting_time=20.0
      frame=webcam_video.get_next_frame()
      _,pointer_location=pointer.detect_pointer(frame)
      if pointer_location==None:
         updateGUI(frame,grid,grid_position,pointer_location=None)
         continue
      pointer_location_inside_grid=convert_pointer_location(pointer_location,grid_position)
      selected_line=grid.findSelectedLine(pointer_location_inside_grid)
      if selected_line==None or line_already_selected(selected_line):
         updateGUI(frame,grid,grid_position,pointer_location)
         continue

      start_time=get_system_time()
      current_time=get_system_time()
      delay=current_time-start_time
      pointer_miss=0
      progress_bar_drawn=False
      while delay<=total_waiting_time:
            frame=webcam_video.get_next_frame()
            _,pointer_location=pointer.detect_pointer(frame)
            if pointer_location==None:
               total_waiting_time=total_waiting_time*1.1
               pointer_miss+=1
               if pointer_miss>max_allowed_pointer_miss:
                  break;
               updateGUI(frame,grid,grid_position,pointer_location=None)
               continue
            pointer_location_inside_grid=convert_pointer_location(pointer_location,grid_position)
            new_selected_line=grid.findSelectedLine(pointer_location_inside_grid)
            if new_selected_line==selected_line:
               grid.drawProgressBarOverLastSelectedLine(delay/total_waiting_time)
               progress_bar_drawn=True
               delay=get_system_time()-start_time
               updateGUI(frame,grid,grid_position,pointer_location)
               continue
            delay=get_system_time()-start_time
            updateGUI(frame,grid,grid_position,pointer_location) 
      if delay>total_waiting_time:
         grid.drawLastSelectedLine()
         progress_bar_drawn=False
         winning_status,player,winning_number,total_number=game_logic(selected_line,player)
         updateGUI(frame,grid,grid_position,pointer_location)
      if progress_bar_drawn==True:
         grid.removeProgressBar()

print game_object.declare_winner()
