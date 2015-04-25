#!/usr/bin/env python

import timeit

from dot import *
from errorhandling import *

# Lines should be lists of dots strictly of size 2
# Boxes should be quadruples of lines starting from roof and continuing clock-wise.
# Have to take care of the fact that the line finalized is not already drawn. Done now.
# Have to incorporate the handling of successive frames. Done now.
# Player to draw the next line should be kept track of. Very IMP. Done now.
# What about the co-ordinates of the dots? Convert to standard unitless Cartesian co-ordinates.

# Line functions

class Grid(object):
    def __init__(self,left_top,grid_size,dot_size):
        self.left_top_dot=dot(left_top)
        self.height_in_dots=grid_size[0]
        self.width_in_dots=grid_size[1]
        self.dot_size=dot_size
        if(self._grid_does_not_fit_in_frame()):
            print "The grid is too big to fit in the frame"
        self.dot_separation=10   #Fixed for the time being

    def denormalize(self,dot):
        pass

    def normalize(self,dot):
        pass

    def _grid_does_not_fit_in_frame(self):
        pass

    def draw_grid_on(self,frame):
        pass

    def not_adjacent(self,dot1,dot2):
        if(self.dot_above(dot1) != dot2 and self.dot_below(dot1) != dot2 and self.dot_to_left_of(dot1) != dot2 and
                self.dot_to_right_of(dot1) != dot2)
            return True
        else:
            return False

    def draw_line(self,line): # line -> list of dots
        if(self.not_adjacent(line[0],line[1])):
            print "Dots not adjacent"
        else:
            pass

    def dot_to_right_of(self,current_dot):
        if(self.is_rightmost(current_dot)):
            return None
        else:
            return(dot(current_dot.get_x()+self.dot_separation,current_dot.get_y()))

    def dot_to_left_of(self,current_dot):
        if(self.is_leftmost(current_dot)):
            return None
        else:
            return(dot(current_dot.get_x()-self.dot_separation,current_dot.get_y()))

    def dot_above(self,current_dot):
        if(self.is_topmost(current_dot)):
            return None
        else:
            return(dot(current_dot.get_x(),current_dot.get_y()+self.dot_separation))

    def dot_below(self,current_dot):
        if(self.is_bottommost(current_dot)):
            return None
        else:
            return(dot(current_dot.get_x(),current_dot.get_y()-self.dot_separation))

