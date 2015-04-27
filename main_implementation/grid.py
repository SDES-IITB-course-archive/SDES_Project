#!/usr/bin/env python

import cv2
import timeit
import numpy as np

from dot import *
from video import *

# Lines should be lists of dots strictly of size 2
# Boxes should be quadruples of lines starting from roof and continuing clock-wise.
# Have to take care of the fact that the line finalized is not already drawn. Done now.
# Have to incorporate the handling of successive frames. Done now.
# Player to draw the next line should be kept track of. Very IMP. Done now.
# What about the co-ordinates of the dots? Convert to standard unitless Cartesian co-ordinates.

# Line functions

class Grid(object):
    def __init__(self,row=4,col=4,dotRadius=4,dotsGap=20,dottype=0,color=(255,0,0)):
#        if(self._grid_does_not_fit_in_frame()):
#            print "The grid is too big to fit in the frame"
# ----------------------------------------------------------------------
        print "hello"
        self.row=row
        self.col=col
        self.dotRadius=dotRadius
        self.dotsGap=dotsGap
        self.dottype=dottype
        self.color=color
        self.height=(row-1)*dotsGap+2*dotRadius
        self.width=(col-1)*dotsGap+2*dotRadius
        self.grid=np.zeros((self.width,self.height,3),np.uint8)
        self.dotPosList=[]
        self.filldots()
        self.linecolor=(0,210,11)
        self.currenLineColor=(112,21,221)
        self.player1boxcolor=(255,128,12)
        self.player2boxcolor=(0,128,12)
        self.lastDrawnLinePos=None

    def filldots(self):
        y=self.dotRadius
        i=0
        while y<self.width:
            x=self.dotRadius
            self.dotPosList.append([])
            while x<self.height:
                if self.dottype==0:
                    cv2.circle(self.grid,(x,y), self.dotRadius, self.color, -1)
                    print "The center of the dot is at ",[x,y]
                else:
                    cv2.rectangle(self.grid,(x-self.dotRadius,y-self.dotRadius),(x+self.dotRadius,y+self.dotRadius), self.color, -1)
                    print "The center of the dot is at ",[x,y]
                self.dotPosList[i].append((x,y))
                x+=self.dotsGap
            y+=self.dotsGap
            i+=1

    def displayGrid(self):
        cv2.imshow("grid window",self.grid)

    #called internally
    def detectHorizontalLine(self,x,y):
        i=0
        noPossibleLine=True
        while i<=self.row-1:
            if y>self.dotPosList[i][0][1]-self.dotRadius and y<self.dotPosList[i][0][1]+self.dotRadius:
                noPossibleLine=False
                break;
            i+=1
        if noPossibleLine==True:
            return None
        j=0
        while j<=self.col-2:
            if x>self.dotPosList[0][j][0]+self.dotRadius and x<self.dotPosList[0][j+1][0]-self.dotRadius:
                return (i,j)
            j+=1
        return None

    #called internally
    def detectVerticalLine(self,x,y):
        j=0
        noPossibleLine=True
        while j<=self.col-1:
            if x>self.dotPosList[0][j][0]-self.dotRadius and x<self.dotPosList[0][j][0]+self.dotRadius:
                noPossibleLine=False
                break;
            j+=1
        if noPossibleLine==True:
            return None
        i=0
        while i<=self.col-2:
           if y>self.dotPosList[i][0][1]+self.dotRadius and y<self.dotPosList[i+1][0][1]-self.dotRadius:
               return (i,j)
           i+=1
        return None

    #called internally
    def isOutsideArea(self,x,y):
        if y<=self.dotPosList[0][0][1]-self.dotRadius or y>=self.dotPosList[self.row-1][0][1]+self.dotRadius \
                or x<=self.dotPosList[0][0][0]-self.dotRadius or x>=self.dotPosList[0][self.col-1][0]+self.dotRadius:
            return True
        else:
            return False

    #this is called to detect if line is selected
    def findSelectedLine(self,x,y):
        print "in findSelectedLine with x and y as ",x,y
        if self.isOutsideArea(x,y):
            return None
        line=self.detectHorizontalLine(x,y)
        if line!=None:
            self.lastSelectedLine=[line,(line[0],line[1]+1)]
            print "the horizontal line is ",self.lastSelectedLine[0],self.lastSelectedLine[1]
            return list(self.lastSelectedLine)
        line=self.detectVerticalLine(x,y)
        if line!=None:
            self.lastSelectedLine=[line,(line[0]+1,line[1])]
            print "the vertical line is ",self.lastSelectedLine[0],self.lastSelectedLine[1]
            return list(self.lastSelectedLine)
        return None

    #called internally
    def drawHorizontalLine(self,line,color):
        startingDotPos=self.dotPosList[line[0].get_x()][line[0].get_y()]
        endingDotPos=self.dotPosList[line[1].get_x()][line[1].get_y()]
        lineTopLeftPos=(startingDotPos[0]+self.dotRadius+1,startingDotPos[1]-self.dotRadius)
        lineBottomRightPos=(endingDotPos[0]-self.dotRadius-1,endingDotPos[1]+self.dotRadius)
        cv2.rectangle(self.grid, lineTopLeftPos, lineBottomRightPos, color, -1)
        return (lineTopLeftPos,lineBottomRightPos)

    #called internally
    def drawVerticalLine(self,line,color):
        startingDotPos=self.dotPosList[line[0].get_x()][line[0].get_y()]
        endingDotPos=self.dotPosList[line[1].get_x()][line[1].get_y()]
        lineTopLeftPos=(startingDotPos[0]-self.dotRadius,startingDotPos[1]+self.dotRadius+1)
        lineBottomRightPos=(endingDotPos[0]+self.dotRadius,endingDotPos[1]-self.dotRadius-1)
        cv2.rectangle(self.grid, lineTopLeftPos, lineBottomRightPos, color, -1)
        return (lineTopLeftPos,lineBottomRightPos)


    #draws a line, this function is called internally
    def drawLine(self,line):
        if self.lastDrawnLinePos!=None:
            cv2.rectangle(self.grid, self.lastDrawnLinePos[0], self.lastDrawnLinePos[1], self.linecolor, -1)
        if line[0].get_x()==line[1].get_x():
            self.lastDrawnLinePos=self.drawHorizontalLine(line,self.currenLineColor)
        else:
            self.lastDrawnLinePos=self.drawVerticalLine(line,self.currenLineColor)


    #this will be called for drawing the last selected line
    def drawLastSelectedLine(self):
        self.drawLine(self.lastSelectedLine)

    #this is called to draw a box
    def drawBox(self,dotCoord,boxcolor=0):
        if boxcolor==0:
            boxcolor=self.player1boxcolor
        else:
            boxcolor=self.player2boxcolor
        startingDotPos=self.dotPosList[dotCoord[0]][dotCoord[1]]
        endingDotPos=self.dotPosList[dotCoord[0]+1][dotCoord[1]+1]
        boxStartPoint=(startingDotPos[0]+self.dotRadius+1,startingDotPos[1]+self.dotRadius+1)
        boxEndPoint=(endingDotPos[0]-self.dotRadius-1,endingDotPos[1]-self.dotRadius-1)
        cv2.rectangle(self.grid,boxStartPoint,boxEndPoint, boxcolor, -1)

    #called internally, not fully implemented
    def blinkHorizontalLine(self,line,color,i):
        self.drawHorizontalLine(line,color=(110,220,40))
        startingDotPos=self.dotPosList[line[0][0]][line[0][1]]
        lineTopLeftPos=(startingDotPos[0]+self.dotRadius,startingDotPos[1]-self.dotRadius)
        lineBottomRightPos=(lineTopLeftPos[0]+int(round(self.dotsGap*(i/2000.0)))-2*self.dotRadius,lineTopLeftPos[1]+2*self.dotRadius)
        print lineTopLeftPos, lineBottomRightPos
        #cv2.rectangle(self.grid, (16,0), lineBottomRightPos, self.currenLineColor, -1)

    #called internally, not fully implemented
    def blinkLastSelectedLine(self,i):
        line=self.lastSelectedLine
        if line[0][0]==line[1][0]:
            self.blinkHorizontalLine(line,self.currenLineColor,i)
        else:
            self.blinkVerticalLine(line,self.currenLineColor,i)

    #not fully implemented
    def blinkTester(self):
        oldline=[(0,0),(0,1)]
        i=0
        while True:
            line=self.findSelectedLine(20,10)
            if line==None:
                i=0
                continue
            if line!=oldline:   # or line==alreadySElectedLIne()
                removeBlinkLastLine()
                i=0
                oldline=line
                continue
            if i<2000:
                i+=1
            self.blinkLastSelectedLine(i)
            self.displayGrid()
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                cv2.destroyWindow("grid window")
                break
    
#    def denormalize(self,dot):
#        pass

#    def normalize(self,dot):
#        pass

    def fill_box(left_top_of_box,owner_of_the_box):
        pass

#    def out_of_grid(dot_under_test):
#        pass

#    def _grid_does_not_fit_in_frame(self):
#        pass

    def draw_grid(self,frame):
        another_frame=self.blendGrid(frame,110,300)
        return frame

    def blendGrid(self,img1,x=210,y=360):
        if img1==None:
            return
        img2=self.grid
        img1=cv2.flip(img1, flipCode=1)
        rows,cols,channels = img2.shape
        roi = img1[x:x+rows, y:y+cols]
        
        img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(img2,img2,mask = mask)

        # Put logo in ROI and modify the main image
        #dst = cv2.addWeighted(img1_bg,0.2,img2_fg,0.8,0)
        img2_fg= cv2.add(img1_bg,img2_fg)
        alpha=0.8
        dst = cv2.addWeighted(roi,1-alpha,img2_fg,alpha,1)
        img1[x:x+rows, y:y+cols ] = dst

#        cv2.imshow("xyzw",img1)
#        cv2.waitKey(10)
#        cv2.imshow("abcd",dst)
#        cv2.waitKey(10)
        return img1
