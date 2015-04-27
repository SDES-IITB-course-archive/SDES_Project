#!/usr/bin/env python

from dot import *

class NormGrid(object):
    def __init__(self,grid_size):
        self.grid_size=grid_size
        self.height=grid_size[0]
        self.width=grid_size[1]

    def not_adjacent(self,dot1,dot2):
        if(self.dot_above(dot1) != dot2 and self.dot_below(dot1) != dot2 and self.dot_to_left_of(dot1) != dot2 and 
                self.dot_to_right_of(dot1) != dot2):
            return True
        else:
            return False

    def is_bottommost(self,dot):
        return(dot.get_x()+1>=self.height)
        
    def is_topmost(self,dot):
        return(dot.get_x()-1<0)
        
    def is_leftmost(self,dot):
        return(dot.get_y()-1<0)

    def is_rightmost(self,dot):
        return(dot.get_y()+1>=self.width)

    def dot_to_right_of(self,current_dot):
        if(self.is_rightmost(current_dot)):
            return None
        else:
            return(Dot([current_dot.get_x(),current_dot.get_y()+1]))

    def dot_to_left_of(self,current_dot):
        if(self.is_leftmost(current_dot)):
            return None
        else:
            return(Dot([current_dot.get_x(),current_dot.get_y()-1]))

    def dot_above(self,current_dot):
        if(self.is_topmost(current_dot)):
            return None
        else:
            return(Dot([current_dot.get_x()-1,current_dot.get_y()]))

    def dot_below(self,current_dot):
        print "step 4"
        if(self.is_bottommost(current_dot)):
            print "step 5"
            return None
        else:
            print "step 6"
            return(Dot([current_dot.get_x()+1,current_dot.get_y()]))
            
    def is_horizontal(self,line):
        left_dot=self.dot_to_left_of(line[1])
        right_dot=self.dot_to_right_of(line[1])
        if(left_dot!=None or right_dot!=None):
            return ((line[0]==left_dot) or (line[0]==right_dot))

    def line_above(self,line):
        if(self.is_horizontal(line)):
            return [self.dot_above(line[0]),self.dot_above(line[1])]

    def line_below(self,line):
        print "step 2 "
        if(self.is_horizontal(line)):
            print "step 3 "
            return [self.dot_below(line[0]),self.dot_below(line[1])]

    def line_to_the_right_of(self,line):
        if(not self.is_horizontal(line)):
            return [self.dot_to_right_of(line[0]),self.dot_to_right_of(line[1])]

    def line_to_the_left_of(self,line):
        if(not self.is_horizontal(line)):
            return [self.dot_to_left_of(line[0]),self.dot_to_left_of(line[1])]

    def pillar_lines(self,roof_line,floor_line):
        left_pillar=[roof_line[0],floor_line[0]]
        right_pillar=[roof_line[1],floor_line[1]]
        return left_pillar,right_pillar

    def roof_and_floor(self,left_pillar,right_pillar):
        roof_line=[left_pillar[0],right_pillar[0]]
        floor_line=[left_pillar[1],right_pillar[1]]
        return roof_line,floor_line
