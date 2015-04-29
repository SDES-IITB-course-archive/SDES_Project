import numpy as np
import cv2
import sys

class GuiGrid(object):
      def __init__(self,row=4,col=4,dot_radius=4,dots_gap=20,dottype=0,color=(255,0,0),\
      fatigue=None,player1_boxcolor=(255,128,12),player2_boxcolor=(0,128,12)):   #dots_gap includes dot_radius
          self.row=row
          self.col=col
          self.dot_radius=dot_radius
          self.dots_gap=dots_gap
          self.dottype=dottype
          self.color=color
          self.height=(row-1)*dots_gap+2*dot_radius
          self.width=(col-1)*dots_gap+2*dot_radius
          self.grid=np.zeros((self.width,self.height,3),np.uint8)
          self.dot_locations=[]
          self.linecolor=(0,210,11)
          self.current_linecolor=(112,21,221)
          self.player1_boxcolor=player1_boxcolor
          self.player2_boxcolor=player2_boxcolor
          self.last_drawn_line_location=None 
          self.last_selected_line=[(0,0),(0,1)] 
          self.progress_bar_drawn_over_line=None 
          self.fatigue=self.assign_fatigue(fatigue)                 
          self.filldots()
          
       
      #called internally    
      def filldots(self):
          if self.dots_gap<2*self.dot_radius:
             raise SizeError("Gap between dots should be greater than 2 dot radius ")
             sys.exit(1)
          y=self.dot_radius
          i=0
          while y<self.width:
            x=self.dot_radius
            self.dot_locations.append([])
            while x<self.height:
              self.create_dot_at(x,y)
              self.dot_locations[i].append((x,y))
              x+=self.dots_gap
            y+=self.dots_gap
            i+=1
     
     
      #called internally
      def create_dot_at(self,x,y):
          if self.dottype==0:
             cv2.circle(self.grid,(x,y), self.dot_radius, self.color, -1)
          else:
             cv2.rectangle(self.grid,(x-self.dot_radius,y-self.dot_radius),(x+self.dot_radius,y+self.dot_radius), self.color, -1) 
     
     
      #called internally
      def display_grid(self):
          cv2.imshow("grid window",self.grid)
      
      
      #called internally
      def assign_fatigue(self,fatigue=None):
          if fatigue==None:
             gap_between_dots=self.dots_gap-2*self.dot_radius
             fatigue=int(gap_between_dots/20)
          return fatigue
             
      #called internally   
      def detect_horizontal_line(self,x,y):
             line_possibility=False
             for i in xrange (self.row):
               if y>self.dot_locations[i][0][1]-self.dot_radius-self.fatigue and y<self.dot_locations[i][0][1]+self.dot_radius+self.fatigue:
                  line_possibility=True
                  break;
             if line_possibility==True:              
               for j in xrange (self.col-1):
                     if x>self.dot_locations[0][j][0]+self.dot_radius and x<self.dot_locations[0][j+1][0]-self.dot_radius:
                        return (i,j)
             return None
      
      #called internally
      def detect_vertical_line(self,x,y):
             line_possibility=False
             for j in xrange(self.col):
               if x>self.dot_locations[0][j][0]-self.dot_radius-self.fatigue and x<self.dot_locations[0][j][0]+self.dot_radius+self.fatigue:
                  line_possibility=True
                  break;
             if line_possibility==True:
                for i in xrange (self.row-1):
                      if y>self.dot_locations[i][0][1]+self.dot_radius and y<self.dot_locations[i+1][0][1]-self.dot_radius:
                         return (i,j)
             return None
      
      #called internally
      def is_outside_area(self,x,y):
           if y<=self.dot_locations[0][0][1]-self.dot_radius or y>=self.dot_locations[self.row-1][0][1]+self.dot_radius \
           or x<=self.dot_locations[0][0][0]-self.dot_radius or x>=self.dot_locations[0][self.col-1][0]+self.dot_radius:
             return True
           else:
             return False
             
      #this is called to detect if line is selected      
      def find_selected_line(self,location,location_y_if_first_arg_is_x=None):
           if location_y_if_first_arg_is_x==None:
              x,y=location[0],location[1]
           else:
              x,y=location,location_y_if_first_arg_is_x
           if self.is_outside_area(x,y):
              return None
              
           starting_dot_of_line=self.detect_horizontal_line(x,y)
           if starting_dot_of_line!=None:
              self.last_selected_line=[starting_dot_of_line,(starting_dot_of_line[0],starting_dot_of_line[1]+1)]
              return self.last_selected_line
              
           starting_dot_of_line=self.detect_vertical_line(x,y)
           if starting_dot_of_line!=None:
              self.last_selected_line=[starting_dot_of_line,(starting_dot_of_line[0]+1,starting_dot_of_line[1])]
              return self.last_selected_line
           return None
           
           
      #called internally     
      def draw_horizontal_line(self,line,color):   
          starting_dot_pos=self.dot_locations[line[0][0]][line[0][1]]
          ending_dot_pos=self.dot_locations[line[1][0]][line[1][1]]
          line_top_left_pos=(starting_dot_pos[0]+self.dot_radius+1,starting_dot_pos[1]-self.dot_radius)
          line_bottom_right_pos=(ending_dot_pos[0]-self.dot_radius-1,ending_dot_pos[1]+self.dot_radius)
          cv2.rectangle(self.grid, line_top_left_pos, line_bottom_right_pos, color, -1)
          return (line_top_left_pos,line_bottom_right_pos)

      #called internally
      def draw_vertical_line(self,line,color):   
          starting_dot_pos=self.dot_locations[line[0][0]][line[0][1]]
          ending_dot_pos=self.dot_locations[line[1][0]][line[1][1]]
          line_top_left_pos=(starting_dot_pos[0]-self.dot_radius,starting_dot_pos[1]+self.dot_radius+1)
          line_bottom_right_pos=(ending_dot_pos[0]+self.dot_radius,ending_dot_pos[1]-self.dot_radius-1)
          cv2.rectangle(self.grid, line_top_left_pos, line_bottom_right_pos, color, -1)
          return (line_top_left_pos,line_bottom_right_pos)

           
      #called internally, it draws a line     
      def draw_line(self,line):
          if self.last_drawn_line_location!=None:
             cv2.rectangle(self.grid, self.last_drawn_line_location[0], self.last_drawn_line_location[1], self.linecolor, -1)
          if line[0][0]==line[1][0]:
             self.last_drawn_line_location=self.draw_horizontal_line(line,self.current_linecolor)
          else:
             self.last_drawn_line_location=self.draw_vertical_line(line,self.current_linecolor)
          
          
      #this will be called for drawing the last selected line         
      def draw_last_selected_line(self):
           self.draw_line(self.last_selected_line)
           
      #this is called to draw a box     
      def draw_box(self,dot_coordinate,boxcolor=0):
          if boxcolor==0:
              boxcolor=self.player1_boxcolor
          else:
              boxcolor=self.player2_boxcolor
          starting_dot_pos=self.dot_locations[dot_coordinate[0]][dot_coordinate[1]]
          ending_dot_pos=self.dot_locations[dot_coordinate[0]+1][dot_coordinate[1]+1]
          box_start_point=(starting_dot_pos[0]+self.dot_radius+1,starting_dot_pos[1]+self.dot_radius+1)
          box_end_point=(ending_dot_pos[0]-self.dot_radius-1,ending_dot_pos[1]-self.dot_radius-1)
          cv2.rectangle(self.grid,box_start_point,box_end_point, boxcolor, -1)
          
      def calculate_bar_length(self,i):
          bar_length=int(round((self.dots_gap-2*self.dot_radius)*i))
          if bar_length<0:
            bar_length=0
          elif bar_length>self.dots_gap-2*self.dot_radius-2:
            bar_length=self.dots_gap-2*self.dot_radius-2
          return bar_length
          
      #called internally
      def draw_horizontal_progress_line(self,line,color,i):
          starting_dot_pos=self.dot_locations[line[0][0]][line[0][1]]
          bar_length=self.calculate_bar_length(i)
          line_top_left_pos=(starting_dot_pos[0]+self.dot_radius+1,starting_dot_pos[1]-self.dot_radius)
          line_bottom_right_pos=(line_top_left_pos[0]+bar_length,line_top_left_pos[1]+2*self.dot_radius)
          cv2.rectangle(self.grid, line_top_left_pos, line_bottom_right_pos, self.current_linecolor, -1)
     
      #called internally
      def draw_vertical_progress_line(self,line,color,i):
          starting_dot_pos=self.dot_locations[line[0][0]][line[0][1]]
          bar_length=self.calculate_bar_length(i)
          line_top_left_pos=(starting_dot_pos[0]-self.dot_radius,starting_dot_pos[1]+self.dot_radius+1)
          line_bottom_right_pos=(line_top_left_pos[0]+2*self.dot_radius,line_top_left_pos[1]+bar_length)
          cv2.rectangle(self.grid, line_top_left_pos, line_bottom_right_pos, self.current_linecolor, -1)
     
      
      
      #called internally
      def draw_progressbar_over_last_selected_line(self,i):
         line=self.last_selected_line
         if line[0][0]==line[1][0]:
             self.draw_horizontal_progress_line(line,self.current_linecolor,i)
         else:
             self.draw_vertical_progress_line(line,self.current_linecolor,i)
         self.progress_bar_drawn_over_line=line
      
      def remove_progress_bar(self):
          line=self.progress_bar_drawn_over_line
          if line==None:
             return
          if line[0][0]==line[1][0]:
             self.draw_horizontal_line(line,(0,0,0))
          else:
             self.draw_vertical_line(line,(0,0,0))
      
      #not fully implemented      
      def blink_tester(self):
         oldline=[(0,0),(0,1)]
         i=0
         max_iteration=1000
         while True:
            line=self.find_selected_line(87,20)
            if line==None:
               i=0
               continue
            if line!=oldline:
               # or line==alreadySElectedLIne()
               self.remove_progress_barOverlast_selected_line()
               i=0
               oldline=line
               continue
            if i<max_iteration:
               i+=1
            self.draw_progressbar_over_last_selected_line(i/float(max_iteration-1))
            self.display_grid()
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
               cv2.destroyWindow("grid window")
               break
            
 
class SizeError(Exception):
      pass
 
 
if __name__=="__main__":
   cv2.namedWindow("grid window", cv2.WINDOW_NORMAL)
   grid =GuiGrid(4,4,8,80,dottype=1)
   grid.draw_line(((1,1),(2,1)))
   grid.draw_line(((0,0),(1,0)))
   grid.draw_line(((0,1),(1,1)))
   grid.draw_line(((2,1),(2,2)))
   grid.draw_line(((3,1),(3,2)))
   grid.draw_box((2,1),boxcolor=0)
   grid.draw_box((1,2),boxcolor=1)   
   grid.blink_tester()
   cv2.namedWindow("grid window", cv2.WINDOW_NORMAL)   
   grid.display_grid()
   key = cv2.waitKey() & 0xFF
   if key == 27:
     cv2.destroyWindow("grid window")
     
    

