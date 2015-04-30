#!/usr/bin/env python

import unittest
import game
import dot

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

# 1) The grid status used in the setUp through the "list_of_lines_drawn" parameter. 
# This is used in the function to test if 2 boxes formed by a single line.

#            (0,1) (0,2) (0,3)
#   (0,0)-------
#        |                 |
#        |                 |
#   (1,0)             ------
#              |     |     |
#              |     |     |
#   (2,0)
#                    |     |
#                    |     |
#   (3,0)-------------------

class TestSquareGame(unittest.TestCase):
    def setUp(self):
        self.rows=4
        self.cols=4
        self.no_of_players=2
        self.mygame=game.Game([self.rows,self.cols],self.no_of_players)

        # Position shown in figure 1)
        self.list_of_lines_drawn=[
                [dot.Dot([0,0]),dot.Dot([0,1])],
                [dot.Dot([1,1]),dot.Dot([2,1])],
                [dot.Dot([3,0]),dot.Dot([3,1])],
                [dot.Dot([3,1]),dot.Dot([3,2])],
                [dot.Dot([3,2]),dot.Dot([3,3])],
                [dot.Dot([1,3]),dot.Dot([2,3])],
                [dot.Dot([1,2]),dot.Dot([1,3])],
                [dot.Dot([0,0]),dot.Dot([1,0])],
                [dot.Dot([0,3]),dot.Dot([1,3])],
                [dot.Dot([2,2]),dot.Dot([3,2])],
                [dot.Dot([2,3]),dot.Dot([3,3])],
                [dot.Dot([1,2]),dot.Dot([2,2])],
        ]

    def tearDown(self):
        del self.rows
        del self.cols
        del self.mygame
        del self.no_of_players
        del self.list_of_lines_drawn

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

    def _quick_check_box(self,list_of_lines_drawn,latest_line,boxlist,box_should_form):
        self.mygame.list_of_lines_drawn=list_of_lines_drawn
        box_formed,boxes=self.mygame.box_formed_by(latest_line)
        if box_should_form:
            self.assertTrue(box_formed)
        else:
            self.assertFalse(box_formed)
        self.assertListEqual(boxes,boxlist)

    def test_box_formed_by(self):
        nonelist=[None,None]
        boxes=[
                  [
                      [dot.Dot([1,2]),dot.Dot([1,3])],
                      [dot.Dot([1,3]),dot.Dot([2,3])],
                      [dot.Dot([2,2]),dot.Dot([2,3])],
                      [dot.Dot([1,2]),dot.Dot([2,2])]
                  ],
                  [
                      [dot.Dot([2,2]),dot.Dot([2,3])],
                      [dot.Dot([2,3]),dot.Dot([3,3])],
                      [dot.Dot([3,2]),dot.Dot([3,3])],
                      [dot.Dot([2,2]),dot.Dot([3,2])]
                  ]
        ]
        self._quick_check_box(self.list_of_lines_drawn,[dot.Dot([2,2]),dot.Dot([2,3])],boxes,True)        
        self._quick_check_box([],[dot.Dot([0,0]),dot.Dot([0,1])],nonelist,False)
        self._quick_check_box(
                                [
                                    [dot.Dot([0,0]),dot.Dot([0,1])],
                                    [dot.Dot([1,0]),dot.Dot([0,0])],
                                    [dot.Dot([0,1]),dot.Dot([1,1])],
                                    [dot.Dot([3,0]),dot.Dot([3,1])]
                                ],
                                [dot.Dot([1,0]),dot.Dot([1,1])],
                                nonelist,False
                             )
        self._quick_check_box(
                                [
                                    [dot.Dot([0,0]),dot.Dot([0,1])],
                                    [dot.Dot([1,0]),dot.Dot([0,0])],
                                    [dot.Dot([0,1]),dot.Dot([1,1])],
                                    [dot.Dot([3,0]),dot.Dot([3,1])]
                                ],
                                [dot.Dot([1,0]),dot.Dot([1,1])],
                                nonelist,False
                             )
        

    def test_set_owner_of_next_line(self):
        pass

    def test_declare_winner(self):
        self._quick_setup_boxes(0,0)
        self.assertEqual(self.mygame.declare_winner(),None)
        self._quick_setup_boxes(4,4)
        self.assertEqual(self.mygame.declare_winner(),None)
        self._quick_setup_boxes(5,4)
        self.assertEqual(self.mygame.declare_winner(),"1")
        self._quick_setup_boxes(4,5)
        self.assertEqual(self.mygame.declare_winner(),"2")
        self._quick_setup_boxes(9,0)
        self.assertEqual(self.mygame.declare_winner(),"1")
        self._quick_setup_boxes(0,9)
        self.assertEqual(self.mygame.declare_winner(),"2")

    def test_update_list_of_drawn_lines_with(self):
        self.mygame.list_of_lines_drawn=[
                                            [dot.Dot([0,0]),dot.Dot([0,1])],
                                            [dot.Dot([0,2]),dot.Dot([0,3])],
                                            [dot.Dot([2,2]),dot.Dot([3,2])],
                                            [dot.Dot([1,2]),dot.Dot([1,3])]
        ]
        self.mygame.update_list_of_drawn_lines_with([dot.Dot([2,0]),dot.Dot([1,0])])
        self.assertNotIn([dot.Dot([2,0]),dot.Dot([1,0])],self.mygame.list_of_lines_drawn)
        self.assertIn([dot.Dot([1,0]),dot.Dot([2,0])],self.mygame.list_of_lines_drawn)
        self.mygame.update_list_of_drawn_lines_with([dot.Dot([2,3]),dot.Dot([2,2])])
        self.assertNotIn([dot.Dot([2,3]),dot.Dot([2,2])],self.mygame.list_of_lines_drawn)
        self.assertIn([dot.Dot([2,2]),dot.Dot([2,3])],self.mygame.list_of_lines_drawn)

    def test_update_no_of_boxes_of_players(self):
        self._quick_setup_boxes(0,0)
        boxes=[None,None]
        self.mygame.update_no_of_boxes_of_players(0,boxes)
        self.assertEqual(self.mygame.no_of_boxes_of_players[0],0)
        self.assertEqual(self.mygame.no_of_boxes_of_players[1],0)
        self.mygame.update_no_of_boxes_of_players(1,boxes)
        self.assertEqual(self.mygame.no_of_boxes_of_players[0],0)
        self.assertEqual(self.mygame.no_of_boxes_of_players[1],0)
        self._quick_setup_boxes(3,4)
        boxes=[
                  [
                      [dot.Dot([0,1]),dot.Dot([0,2])],
                      [dot.Dot([0,2]),dot.Dot([1,2])],
                      [dot.Dot([1,1]),dot.Dot([1,2])],
                      [dot.Dot([0,1]),dot.Dot([1,1])]
                  ],
                  [
                      [dot.Dot([0,2]),dot.Dot([0,3])],
                      [dot.Dot([1,2]),dot.Dot([1,3])],
                      [dot.Dot([0,3]),dot.Dot([1,3])],
                      [dot.Dot([0,2]),dot.Dot([1,2])]
                  ]
        ]
        self.mygame.update_no_of_boxes_of_players(0,boxes)
        self.assertEqual(self.mygame.no_of_boxes_of_players[0],4)
        self.assertEqual(self.mygame.no_of_boxes_of_players[1],4)
        [box1,_]=boxes
        self._quick_setup_boxes(4,2)
        self.mygame.update_no_of_boxes_of_players(1,[box1,None])
        self.assertEqual(self.mygame.no_of_boxes_of_players[0],4)
        self.assertEqual(self.mygame.no_of_boxes_of_players[1],3)

if __name__ == '__main__':
    unittest.main()
