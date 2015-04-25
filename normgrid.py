#!/usr/bin/env python

from dot import *

class NormGrid(object):
    def __init__(self,grid_size):
        self.grid_size=grid_size
        self.grid=

    def not_adjacent(self,dot1,dot2):
        if(self.dot_above(dot1) != dot2 and self.dot_below(dot1) != dot2 and self.dot_to_left_of(dot1) != dot2 and
                self.dot_to_right_of(dot1) != dot2)
            return True
        else:
            return False

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
