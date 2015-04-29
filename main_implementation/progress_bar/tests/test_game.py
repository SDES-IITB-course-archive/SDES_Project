#!/usr/bin/env python

import unittest
import game
import dot

class TestSquareGame(unittest.TestCase):
    def setUp(self):
        self.rows=4
        self.cols=4
        self.no_of_players=2
        self.mygame=game.Game([self.rows,self.cols],self.no_of_players)

    def tearDown(self):
        del self.rows
        del self.cols
        del self.mygame
        del self.no_of_players

    def _quick_setup_boxes(self,player1_boxes,player2_boxes):
        self.mygame.no_of_boxes_of_players[0]=player1_boxes
        self.mygame.no_of_boxes_of_players[1]=player2_boxes

    def test_game_ended(self):
        self._quick_setup_boxes(0,0)
        self.assertFalse(self.mygame.game_ended())
        self._quick_setup_boxes(4,9)
        self.assertRaises(game.LogicError,self.mygame.game_ended)
        self._quick_setup_boxes(8,9)
        self.assertRaises(game.LogicError,self.mygame.game_ended)
        self._quick_setup_boxes(8,1)
        self.assertTrue(self.mygame.game_ended())
        self._quick_setup_boxes(7,2)
        self.assertTrue(self.mygame.game_ended())
        self._quick_setup_boxes(0,8)
        self.assertFalse(self.mygame.game_ended())
        self._quick_setup_boxes(1,-2)
        self.assertRaises(game.LogicError,self.mygame.game_ended)

    def _quick_check_box(self,list_of_lines_drawn,latest_line,boxlist):
        self.mygame.list_of_lines_drawn=list_of_lines_drawn
        box_formed,boxes=self.mygame.box_formed_by(latest_line)
        self.assertFalse(box_formed)
        self.assertListEqual(boxes,boxlist)

    def test_box_formed_by(self):
        nonelist=[None,None]
        _quick_check_box([],[dot.Dot([0,0]),dot.Dot([0,1])],nonelist):
        _quick_check_box([[dot.Dot([0,0]),dot.Dot([0,1])],[dot.Dot([1,0]),dot.Dot([0,0])],[dot.Dot([0,1]),dot.Dot([1,1])],[dot.Dot([3,0]),dot.Dot([3,1])]],[dot.Dot([1,0]),dot.Dot([1,1])],nonelist):
        _quick_check_box([[dot.Dot([0,0]),dot.Dot([0,1])],[dot.Dot([1,0]),dot.Dot([0,0])],[dot.Dot([0,1]),dot.Dot([1,1])],[dot.Dot([3,0]),dot.Dot([3,1])]],[dot.Dot([1,0]),dot.Dot([1,1])],nonelist):        
        

#            (0,1) (0,2) (0,3)
#   (0,0)-------------------
#        |     |     |     |
#        |     |     |     |
#   (1,0)-------------------
#        |     |     |     |
#        |     |     |     |
#   (2,0)-------------------
#        |     |     |     |
#        |     |     |     |
#   (3,0)-------------------
    def test_set_owner_of_next_line(self):
        pass
    def test_declare_winner(self):
        pass
    def test_update_list_of_drawn_lines_with(self):
        pass
    def test_update_no_of_boxes_of_players(self):
        pass
    def test_(self):
        pass
class TestRectGame(unittest.TestCase):
    def setUp(self):
        self.rows=3
        self.cols=5
        self.no_of_players=2
        self.mygame=game.Game([self.rows,self.cols],self.no_of_players)

    def tearDown(self):
        del self.rows
        del self.cols
        del self.mygame
        del self.no_of_players

    def test_game_ended(self):
        pass


    def test_box_formed_by(self):
        pass
    def test_set_owner_of_next_line(self):
        pass
    def test_declare_winner(self):
        pass
    def test_update_list_of_drawn_lines_with(self):
        pass
    def test_update_no_of_boxes_of_players(self):
        pass
    def test_(self):
        pass
if __name__ == '__main__':
    unittest.main()
