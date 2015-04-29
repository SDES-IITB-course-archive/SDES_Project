#!/usr/bin/env python

# Lines should be lists of dots strictly of size 2
# Boxes should be quadruples of lines starting from roof and continuing clock-wise.
# Have to take care of the fact that the line finalized is not already drawn. Done now.
# Have to incorporate the handling of successive frames. Done now.
# Player to draw the next line should be kept track of. Very IMP. Done now.
# What about the co-ordinates of the dots? Convert to standard unitless Cartesian co-ordinates.

from normgrid import *

class LogicError(Exception):
    pass

class Game(object):
    def __init__(self,grid_size,no_of_players):
        self.new_grid=NormGrid(grid_size)
        self.grid_size=grid_size
        self.no_of_players=no_of_players
        self.owner_of_next_line=0
        self.owner_of_last_line=self.no_of_players-1
        self.list_of_lines_drawn=[]
        self.no_of_boxes_of_players=[0,0]

    def _grid_filled(self):
        total_no_of_boxes=sum(self.no_of_boxes_of_players)
        maximum_no_of_boxes=(self.grid_size[0]-1)*(self.grid_size[1]-1)
        if(total_no_of_boxes>maximum_no_of_boxes or total_no_of_boxes<0):
            raise LogicError
        return total_no_of_boxes==maximum_no_of_boxes

    def game_ended(self):
        return self._grid_filled()

    def set_owner_of_next_line(self,box_formed):
        if not box_formed:
            self.owner_of_next_line=self.player_next_to(self.owner_of_next_line)
            self.owner_of_last_line=self.player_next_to(self.owner_of_last_line)
        else:
            self.owner_of_next_line=self.owner_of_next_line
            self.owner_of_last_line=self.owner_of_next_line

    def player_next_to(self,player):
        return (player+1)%self.no_of_players

    def get_owner_of_next_line(self):
        return self.owner_of_next_line

    def declare_winner(self):
        if(self.no_of_boxes_of_players[0]>self.no_of_boxes_of_players[1]):
            winner="1"
        elif(self.no_of_boxes_of_players[0]<self.no_of_boxes_of_players[1]):
            winner="2"
        else:
            winner=None
        return winner
             
    def update_no_of_boxes_of_players(self,owner_of_the_box,boxes):
        no_of_boxes=0
        for i in range(0,2):
            if(boxes[i]!=None):
                left_pillar,right_pillar=self.new_grid.pillar_lines(boxes[i][0],boxes[i][2])
                if(([left_pillar,right_pillar])==[boxes[i][3],boxes[i][1]]):
                    no_of_boxes+=1
        self.no_of_boxes_of_players[owner_of_the_box]+=no_of_boxes

    def get_owner_of_last_line(self):
        return self.owner_of_last_line

    def update_list_of_drawn_lines_with(self,latest_line): # Update the list with the lines expressed in the correct format,i.e.,top-to-bottom or left-to-right
        if(self.new_grid.is_horizontal(latest_line)):
            if(latest_line[0]!=self.new_grid.dot_to_left_of(latest_line[1])):
                latest_line=latest_line[::-1]
            self.list_of_lines_drawn.append(latest_line)
            return
        else:
            if(latest_line[0]!=self.new_grid.dot_above(latest_line[1])):
                latest_line=latest_line[::-1]
            self.list_of_lines_drawn.append(latest_line)
            return

    def box_formed_by(self,latest_line):
        box_formed=False
        box1=None
        box2=None
        if(self.new_grid.is_horizontal(latest_line)):
            if(self.new_grid.line_above(latest_line) in self.list_of_lines_drawn):
                left_pillar,right_pillar=self.new_grid.pillar_lines(self.new_grid.line_above(latest_line),latest_line)
                if((left_pillar in self.list_of_lines_drawn) and (right_pillar in self.list_of_lines_drawn)):
                    box_formed=True
                    box1=[self.new_grid.line_above(latest_line),right_pillar,latest_line,left_pillar]
            if(self.new_grid.line_below(latest_line) in self.list_of_lines_drawn):
                left_pillar,right_pillar=self.new_grid.pillar_lines(latest_line,self.new_grid.line_below(latest_line))
                if((left_pillar in self.list_of_lines_drawn) and (right_pillar in self.list_of_lines_drawn)):
                    box_formed=True
                    box2=[latest_line,right_pillar,self.new_grid.line_below(latest_line),left_pillar]
            return box_formed,[box1,box2]
        else:
            if(self.new_grid.line_to_the_left_of(latest_line) in self.list_of_lines_drawn):
                roof,floor=self.new_grid.roof_and_floor(self.new_grid.line_to_the_left_of(latest_line),latest_line)
                if((roof in self.list_of_lines_drawn) and (floor in self.list_of_lines_drawn)):
                    box_formed=True
                    box1=[roof,latest_line,floor,self.new_grid.line_to_the_left_of(latest_line)]
            if(self.new_grid.line_to_the_right_of(latest_line) in self.list_of_lines_drawn):
                roof,floor=self.new_grid.roof_and_floor(latest_line,self.new_grid.line_to_the_right_of(latest_line))
                if((roof in self.list_of_lines_drawn) and (floor in self.list_of_lines_drawn)):
                    box_formed=True
                    box2=[roof,self.new_grid.line_to_the_right_of(latest_line),floor,latest_line]
            return box_formed,[box1,box2]
