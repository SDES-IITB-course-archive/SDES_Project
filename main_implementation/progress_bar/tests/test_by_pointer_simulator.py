import random
import guigrid
import cv2
import time
import sys

def pointGenerator(xmax,ymax,sigma=2):
    x,y=random.randint(0,xmax),random.randint(0,ymax)
    while True:
          if x>xmax or y>ymax:
             x,y=random.randint(0,xmax),random.randint(0,ymax)
             yield (x,y)
          x,y=int(random.gauss(x,sigma)),int(random.gauss(y,sigma))
          yield (x,y)


def getGaussian(pointer_location,sigma):
    gaussian_new_point=int(random.gauss(pointer_location[0],sigma)),int(random.gauss(pointer_location[1],sigma))
    return gaussian_new_point
    
def update_gui(grid,pointer_location):
    display=grid.grid.copy()
    cv2.circle(display,pointer_location,6,(255,255,255),-1)
    cv2.imshow("grid window",display)
    key = cv2.waitKey(1)
    if key == 27:
       cv2.destroyWindow("grid window")
       sys.exit(1)


def line_already_drawn(line,drawn_lines):
    if line in drawn_lines:
       return True
    else:
       return False

def get_system_time():
    return time.time()

#not fully implemented
def test_line_drawing_by_pointer_simulator():
    total_waiting_time=0.2
    grid =guigrid.GuiGrid(6,6,10,80,dottype=1)
    pointer=pointGenerator(grid.width,grid.height,sigma=10)
    drawn_lines=[]
    progress_bar_drawn=False
    
    while True:
          pointer_location=pointer.next()
          line=grid.find_selected_line(pointer_location)
          if line==None or line_already_drawn(line,drawn_lines):
             update_gui(grid,pointer_location)
             continue
          start_time=get_system_time()
          delay=0
          while delay<=total_waiting_time:
                pointer_location=getGaussian(pointer_location,sigma=1)
                new_line=grid.find_selected_line(pointer_location)
                if new_line==line:
		   grid.draw_progressbar_over_last_selected_line(delay/total_waiting_time)
	           progress_bar_drawn=True
                   delay=get_system_time()-start_time
	           update_gui(grid,pointer_location)
	           continue
	        else:
		   update_gui(grid,pointer_location) 
		   break
	  if delay>total_waiting_time:
             grid.draw_last_selected_line()
             drawn_lines.append(line)
             progress_bar_drawn=False
             update_gui(grid,pointer_location)
	  if progress_bar_drawn==True:
	        grid.remove_progress_bar()
    
if __name__=="__main__":
   test_line_drawing_by_pointer_simulator()    

