from Tkinter import *
from Canvas import Rectangle
from board import GameBoard

def cartesian( v1, v2 ):
    """ Helper function
    returns cartesian product of the two
    'sets' v1, v2"""
    return tuple([(x,y) for x in v1 for y in v2])


def right(x):
    """Helper function: argument x must be a dot.
    Returns dot right of x."""
    return (x[0]+1,x[1])


def upper(x):
    """Helper function: argument x must be a dot.
    Returns dot above (actually below) x."""
    return (x[0], x[1]+1)


class GameGUI:
    def __init__(self, board):
        """Initializes graphic display of a rectangular gameboard."""
        # Properties of gameboard
        dw = self.dotwidth = 6
        sw = self.squarewidth = 60
        sk = self.skip = 4
        fw = self.fieldwidth = dw + sw + 2*sk
        ins = self.inset = sw/2
        self.barcolors = ['red','blue']
        self.squarecolors = ['orange', 'lightblue']

        # Construct Canvas
        self.board = board
        width, height = board.width, board.height
        # compute size of canvas:
        w = width * fw
        h = height * fw
        self.root = Tk()
        cv = self.cv = Canvas(self.root, width=w, height=h, bg='white')
        cv.bind('<Button-1>', self._callback)
        cv.pack()

        # Put geometrical objects - dots, bars and squares - on canvas
        self.bars = {}
        self.squares = {}
        for dot in cartesian(range(width), range(height)):
            # dots. Never used again
            Rectangle( cv, ins+dot[0]*fw,      ins+dot[1]*fw,
                           ins+dot[0]*fw + dw, ins+dot[1]*fw + dw,
                       fill='black', outline='' )
            # horizontal bars
            if dot[0] < width - 1:
                x0 = ins+dot[0]*fw+dw+sk
                y0 = ins+dot[1]*fw
                self.bars[(dot,right(dot))] =\
                                            Rectangle(cv,x0,y0,x0+sw,y0+dw,fill='lightgray',outline='')
            # vertical bars
            if dot[1] < height - 1:
                x0 = ins+dot[0]*fw
                y0 = ins+dot[1]*fw + dw + sk
                self.bars[(dot,upper(dot))] =\
                                            Rectangle(cv,x0,y0,x0+dw,y0+sw,fill='lightgray',outline='')
            # squares
            if (dot[0] < width - 1) and (dot[1] < height - 1):
                x0 =ins+dot[0]*fw + dw + sk
                y0 =ins+dot[1]*fw + dw + sk
                self.squares[dot] = \
                                  Rectangle(cv,x0,y0,x0+sw,y0+sw,fill='lightyellow',outline='')
        cv.update()
        self.root.mainloop()

    def _coord(self,x):
        """returns pixel-coordinate corresponding to
        a dot-coordinate x"""
        return self.inset + self.dotwidth/2 + self.fieldwidth*x

    def _find_bar(self,event):
        """returns bar next to mouse-position when clicked,
        if applicable, otherwise None"""
        ex, ey = event.x, event.y
        for bar in self.bars:
            ((x1,y1),(x2,y2))=bar
            mx, my = ( (self._coord(x1)+self._coord(x2))/2,
                       (self._coord(y1)+self._coord(y2))/2 )
            if abs(ex-mx)+abs(ey-my) < self.squarewidth/2:
                return bar

    def _callback(self, event):
        """Action following a mouse-click"""
        hit = self._find_bar(event)
        board = self.board
        print "Hit:", hit
        if not hit or board.isGameOver() or board.board.has_key(hit):
            return
        # Do a move
        player = board.getPlayer()
        print "Turn %d (Player %s)" % (board.turn, player)
        self.bars[hit]['fill']=self.barcolors[player]
        targets = board.play(hit)
        print "Targets:", targets
        if targets:
            for target in targets:
                print "Square completed.", board.squares[target]
                self.squares[target]['fill'] = self.squarecolors[player]
                board.scores[player] += 1
        board.turn = board.turn + 1
        print "\n"
        if board.isGameOver():
            print "Game over!"
            print "Final board position:"
            print board
            print
            print "Final score:\n\tPlayer 0: %s\n\tPlayer 1: %s" % \
                                tuple(board.scores)


def _gtest(width, height):
    """A small driver to make sure that the board works.  It's not
    safe to use this test function in production, because it uses
    input()."""
    print "Running _gtest... "
    board = GameBoard(width, height)
    board.turn = 1
    board.scores = [0, 0]
    gui = GameGUI(board)


if __name__ == '__main__':
    # graphics mode
    if len(sys.argv[1:]) == 2:
        _gtest(int(sys.argv[1]), int(sys.argv[2]))
    elif len(sys.argv[1:]) == 1:
        _gtest(int(sys.argv[1]), int(sys.argv[1]))
    else:
        _gtest(5, 5)
