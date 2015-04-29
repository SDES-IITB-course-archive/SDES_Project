#!/usr/bin/env python

import unittest
import dot
import normgrid

class TestNormGrid(unittest.TestCase):
    def setUp(self):
        self.grid_size=[4,4]
        self.height=self.grid_size[0]
        self.width=self.grid_size[1]
        self.mygrid=normgrid.NormGrid(self.grid_size)

    def tearDown(self):
        del self.grid_size
        del self.height
        del self.width
        del self.mygrid

    def test_not_adjacent(self):
        self.assertFalse(self.mygrid.not_adjacent(dot.Dot([1,2]),dot.Dot([2,2])))
        self.assertTrue(self.mygrid.not_adjacent(dot.Dot([2,2]),dot.Dot([2,2])))
        self.assertFalse(self.mygrid.not_adjacent(dot.Dot([2,1]),dot.Dot([3,1])))
        self.assertTrue(self.mygrid.not_adjacent(dot.Dot([1,1]),dot.Dot([2,2])))

    def test_is_bottommost(self):
        self.assertFalse(self.mygrid.is_bottommost(dot.Dot([1,2])))
        self.assertFalse(self.mygrid.is_bottommost(dot.Dot([0,0])))
        self.assertTrue(self.mygrid.is_bottommost(dot.Dot([3,3])))
        self.assertTrue(self.mygrid.is_bottommost(dot.Dot([3,0])))
        self.assertFalse(self.mygrid.is_bottommost(dot.Dot([0,3])))

    def test_is_topmost(self):
        self.assertFalse(self.mygrid.is_topmost(dot.Dot([1,0])))
        self.assertFalse(self.mygrid.is_topmost(dot.Dot([3,3])))
        self.assertTrue(self.mygrid.is_topmost(dot.Dot([0,0])))
        self.assertTrue(self.mygrid.is_topmost(dot.Dot([0,3])))
        self.assertFalse(self.mygrid.is_topmost(dot.Dot([2,1])))

    def test_is_leftmost(self):
        self.assertFalse(self.mygrid.is_leftmost(dot.Dot([1,1])))
        self.assertFalse(self.mygrid.is_leftmost(dot.Dot([3,3])))
        self.assertTrue(self.mygrid.is_leftmost(dot.Dot([0,0])))
        self.assertTrue(self.mygrid.is_leftmost(dot.Dot([1,0])))
        self.assertTrue(self.mygrid.is_leftmost(dot.Dot([2,0])))

    def test_is_rightmost(self):
        self.assertFalse(self.mygrid.is_rightmost(dot.Dot([1,1])))
        self.assertFalse(self.mygrid.is_rightmost(dot.Dot([0,0])))
        self.assertTrue(self.mygrid.is_rightmost(dot.Dot([3,3])))
        self.assertTrue(self.mygrid.is_rightmost(dot.Dot([2,3])))
        self.assertTrue(self.mygrid.is_rightmost(dot.Dot([0,3])))

    def test_dot_to_right_of(self):
        self.assertEqual(self.mygrid.dot_to_right_of(dot.Dot([0,1])),dot.Dot([0,2]))
        self.assertIsNone(self.mygrid.dot_to_right_of(dot.Dot([0,3])))
        self.assertEqual(self.mygrid.dot_to_right_of(dot.Dot([3,2])),dot.Dot([3,3]))
        self.assertEqual(self.mygrid.dot_to_right_of(dot.Dot([0,0])),dot.Dot([0,1]))
        self.assertIsNone(self.mygrid.dot_to_right_of(dot.Dot([3,3])))

    def test_dot_to_left_of(self):
        self.assertEqual(self.mygrid.dot_to_left_of(dot.Dot([0,1])),dot.Dot([0,0]))
        self.assertIsNone(self.mygrid.dot_to_left_of(dot.Dot([0,0])))
        self.assertEqual(self.mygrid.dot_to_left_of(dot.Dot([2,2])),dot.Dot([2,1]))
        self.assertEqual(self.mygrid.dot_to_left_of(dot.Dot([3,1])),dot.Dot([3,0]))
        self.assertIsNone(self.mygrid.dot_to_left_of(dot.Dot([3,0])))

    def test_dot_above(self):
        self.assertEqual(self.mygrid.dot_above(dot.Dot([1,1])),dot.Dot([0,1]))
        self.assertIsNone(self.mygrid.dot_above(dot.Dot([0,3])))
        self.assertEqual(self.mygrid.dot_above(dot.Dot([3,0])),dot.Dot([2,0]))
        self.assertEqual(self.mygrid.dot_above(dot.Dot([2,2])),dot.Dot([1,2]))
        self.assertIsNone(self.mygrid.dot_above(dot.Dot([0,0])))

    def test_dot_below(self):
        self.assertEqual(self.mygrid.dot_below(dot.Dot([0,1])),dot.Dot([1,1]))
        self.assertIsNone(self.mygrid.dot_below(dot.Dot([3,3])))
        self.assertEqual(self.mygrid.dot_below(dot.Dot([2,2])),dot.Dot([3,2]))
        self.assertEqual(self.mygrid.dot_below(dot.Dot([1,3])),dot.Dot([2,3]))
        self.assertIsNone(self.mygrid.dot_below(dot.Dot([3,0])))

    def test_is_horizontal(self):
        self.assertFalse(self.mygrid.is_horizontal([dot.Dot([0,0]),dot.Dot([1,0])]))
        self.assertTrue(self.mygrid.is_horizontal([dot.Dot([0,0]),dot.Dot([0,1])]))
        self.assertTrue(self.mygrid.is_horizontal([dot.Dot([3,2]),dot.Dot([3,3])]))
        self.assertFalse(self.mygrid.is_horizontal([dot.Dot([3,3]),dot.Dot([2,3])]))
        self.assertTrue(self.mygrid.is_horizontal([dot.Dot([2,2]),dot.Dot([2,1])]))
                
    def test_line_above(self):
        self.assertEqual(self.mygrid.line_above([dot.Dot([2,0]),dot.Dot([2,1])]),[dot.Dot([1,0]),dot.Dot([1,1])])
        self.assertEqual(self.mygrid.line_above([dot.Dot([0,0]),dot.Dot([0,1])]),[None,None])
        self.assertEqual(self.mygrid.line_above([dot.Dot([3,3]),dot.Dot([3,2])]),[dot.Dot([2,3]),dot.Dot([2,2])])
        self.assertEqual(self.mygrid.line_above([dot.Dot([2,2]),dot.Dot([2,3])]),[dot.Dot([1,2]),dot.Dot([1,3])])
        self.assertIsNone(self.mygrid.line_above([dot.Dot([0,0]),dot.Dot([1,1])]))
        
    def test_line_below(self):
        self.assertEqual(self.mygrid.line_below([dot.Dot([0,0]),dot.Dot([0,1])]),[dot.Dot([1,0]),dot.Dot([1,1])])
        self.assertEqual(self.mygrid.line_below([dot.Dot([3,0]),dot.Dot([3,1])]),[None,None])
        self.assertEqual(self.mygrid.line_below([dot.Dot([2,2]),dot.Dot([2,3])]),[dot.Dot([3,2]),dot.Dot([3,3])])
        self.assertEqual(self.mygrid.line_below([dot.Dot([0,3]),dot.Dot([0,2])]),[dot.Dot([1,3]),dot.Dot([1,2])])
        self.assertEqual(self.mygrid.line_below([dot.Dot([3,3]),dot.Dot([3,2])]),[None,None])

    def test_line_to_the_right_of(self):
        self.assertEqual(self.mygrid.line_to_the_right_of([dot.Dot([0,1]),dot.Dot([1,1])]),[dot.Dot([0,2]),dot.Dot([1,2])])
        self.assertIsNone(self.mygrid.line_to_the_right_of([dot.Dot([0,0]),dot.Dot([0,1])]))
        self.assertEqual(self.mygrid.line_to_the_right_of([dot.Dot([2,2]),dot.Dot([3,2])]),[dot.Dot([2,3]),dot.Dot([3,3])])
        self.assertEqual(self.mygrid.line_to_the_right_of([dot.Dot([1,2]),dot.Dot([2,2])]),[dot.Dot([1,3]),dot.Dot([2,3])])
        self.assertIsNone(self.mygrid.line_to_the_right_of([dot.Dot([0,3]),dot.Dot([0,2])]))

    def test_pillar_lines(self):
        roof=[dot.Dot([1,2]),dot.Dot([1,3])]
        floor=[dot.Dot([2,2]),dot.Dot([2,3])]
        left_pillar,right_pillar=self.mygrid.pillar_lines(roof,floor)
        self.assertEqual(roof[0],left_pillar[0])
        self.assertEqual(roof[1],right_pillar[0])
        self.assertEqual(floor[0],left_pillar[1])
        self.assertEqual(floor[0],left_pillar[1])
       
    def test_roof_and_floor(self):
        left_pillar=[dot.Dot([2,2]),dot.Dot([3,2])]
        right_pillar=[dot.Dot([2,3]),dot.Dot([3,3])]
        roof,floor=self.mygrid.roof_and_floor(left_pillar,right_pillar)
        self.assertEqual(roof[0],left_pillar[0])
        self.assertEqual(roof[1],right_pillar[0])
        self.assertEqual(floor[0],left_pillar[1])
        self.assertEqual(floor[0],left_pillar[1])
       
if __name__ == '__main__':
    unittest.main()
