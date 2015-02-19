# SDES_Project
This project is to develop "the dot and box" game based on augmented reality in Python. A webcam will be used to detect a rectangle drawn on a real surface and then a dot grid will be simulated over the rectangle to play the game. A typical game will follow the following course of events.

1) At the start of the game, players will be asked for their initials and the size of the grid of dots they want to play with.
2) On the basis of this value and the rectangular frame (drawn on a plane surface on which the game will be played) detected by the webcam, the webcam output on the screen will show a grid of dots, drawn aligned with the frame (i.e. 4 outer sides of the grid will overlap with the frame). 
    - The detection of the frame and simulation of the grid will be achieved with the help of the PyARTK which is an open source Python wrapper for ARToolKit.
3) With the help of a unique colored pointer, player 1 will tap on a dot of his/her choice in the grid.
    - The real challenge lies in this motion detection. But, again, PyARTK will be used here.
4) Next, the same player will tap on any one of the 4 dots immediately adjacent to the earlier dot (not diagonally) and a line will be drawn between these 2 dots.
5) If this line forms a box(es), then the player's initials will appear inside that box(es).
6) A player gets a chance to play again if he/she completes a box.
7) When all the boxes are complete the player with most boxes wins.

Points 1-4 above will involve heavy use of the library PyARTK.
Points 5-7 will involve the algorithm designing by us.
