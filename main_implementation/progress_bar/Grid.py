import numpy as np
import cv2
import sys

class Grid(object):
      def __init__(self,row=4,col=4,dotRadius=4,dotsGap=20,dottype=0,color=(255,0,0),\
      fatigue=None,player1boxcolor=(255,128,12),player2boxcolor=(0,128,12)):   #dotsGap includes dotRadius
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
          self.linecolor=(0,210,11)
          self.currenLineColor=(112,21,221)
          self.player1boxcolor=player1boxcolor
          self.player2boxcolor=player2boxcolor
          self.lastDrawnLinePos=None 
          self.lastSelectedLine=[(0,0),(0,1)] 
          self.progress_bar_drawn_over_line=None 
          self.fatigue=self.assignFatigue(fatigue)                 
          self.filldots()
          
       
      #called internally    
      def filldots(self):
          if self.dotsGap<2*self.dotRadius:
             print "Gap between dots should be greater than 2 dot radius "
             sys.exit(1)
          y=self.dotRadius
          i=0
          while y<self.width:
            x=self.dotRadius
            self.dotPosList.append([])
            while x<self.height:
              self.createDotAt(x,y)
              self.dotPosList[i].append((x,y))
              x+=self.dotsGap
            y+=self.dotsGap
            i+=1
     
     
      #called internally
      def createDotAt(self,x,y):
          if self.dottype==0:
             cv2.circle(self.grid,(x,y), self.dotRadius, self.color, -1)
          else:
             cv2.rectangle(self.grid,(x-self.dotRadius,y-self.dotRadius),(x+self.dotRadius,y+self.dotRadius), self.color, -1) 
     
     
      #called internally
      def displayGrid(self):
          cv2.imshow("grid window",self.grid)
      
      
      
      def assignFatigue(self,fatigue=None):
          if fatigue==None:
             gap_between_dots=self.dotsGap-2*self.dotRadius
             fatigue=int(gap_between_dots/20)
          return fatigue
             
      #called internally   
      def detectHorizontalLine(self,x,y):
             linePossibility=False
             for i in xrange (self.row):
               if y>self.dotPosList[i][0][1]-self.dotRadius-self.fatigue and y<self.dotPosList[i][0][1]+self.dotRadius+self.fatigue:
                  linePossibility=True
                  break;
             if linePossibility==True:              
               for j in xrange (self.col-1):
                     if x>self.dotPosList[0][j][0]+self.dotRadius and x<self.dotPosList[0][j+1][0]-self.dotRadius:
                        return (i,j)
             return None
      
      #called internally
      def detectVerticalLine(self,x,y):
             linePossibility=False
             for j in xrange(self.col):
               if x>self.dotPosList[0][j][0]-self.dotRadius-self.fatigue and x<self.dotPosList[0][j][0]+self.dotRadius+self.fatigue:
                  linePossibility=True
                  break;
             if linePossibility==True:
                for i in xrange (self.row-1):
                      if y>self.dotPosList[i][0][1]+self.dotRadius and y<self.dotPosList[i+1][0][1]-self.dotRadius:
                         return (i,j)
             return None
      
      #called internally
      def isOutsideArea(self,x,y):
           if y<=self.dotPosList[0][0][1]-self.dotRadius or y>=self.dotPosList[self.row-1][0][1]+self.dotRadius \
           or x<=self.dotPosList[0][0][0]-self.dotRadius or x>=self.dotPosList[0][self.col-1][0]+self.dotRadius:
             return True
           else:
             return False
             
      #this is called to detect if line is selected      
      def findSelectedLine(self,location,location_y_if_first_arg_is_x=None):
           if location_y_if_first_arg_is_x==None:
              x,y=location[0],location[1]
           else:
              x,y=location,location_y_if_first_arg_is_x
           if self.isOutsideArea(x,y):
              return None
              
           startingDotOfLine=self.detectHorizontalLine(x,y)
           if startingDotOfLine!=None:
              self.lastSelectedLine=[startingDotOfLine,(startingDotOfLine[0],startingDotOfLine[1]+1)]
              return self.lastSelectedLine
              
           startingDotOfLine=self.detectVerticalLine(x,y)
           if startingDotOfLine!=None:
              self.lastSelectedLine=[startingDotOfLine,(startingDotOfLine[0]+1,startingDotOfLine[1])]
              return self.lastSelectedLine
           return None
           
           
      #called internally     
      def drawHorizontalLine(self,line,color):   
          startingDotPos=self.dotPosList[line[0][0]][line[0][1]]
          endingDotPos=self.dotPosList[line[1][0]][line[1][1]]
          lineTopLeftPos=(startingDotPos[0]+self.dotRadius+1,startingDotPos[1]-self.dotRadius)
          lineBottomRightPos=(endingDotPos[0]-self.dotRadius-1,endingDotPos[1]+self.dotRadius)
          cv2.rectangle(self.grid, lineTopLeftPos, lineBottomRightPos, color, -1)
          return (lineTopLeftPos,lineBottomRightPos)

      #called internally
      def drawVerticalLine(self,line,color):   
          startingDotPos=self.dotPosList[line[0][0]][line[0][1]]
          endingDotPos=self.dotPosList[line[1][0]][line[1][1]]
          lineTopLeftPos=(startingDotPos[0]-self.dotRadius,startingDotPos[1]+self.dotRadius+1)
          lineBottomRightPos=(endingDotPos[0]+self.dotRadius,endingDotPos[1]-self.dotRadius-1)
          cv2.rectangle(self.grid, lineTopLeftPos, lineBottomRightPos, color, -1)
          return (lineTopLeftPos,lineBottomRightPos)

           
      #draws a line, this function is called internally    
      def drawLine(self,line):
          if self.lastDrawnLinePos!=None:
             cv2.rectangle(self.grid, self.lastDrawnLinePos[0], self.lastDrawnLinePos[1], self.linecolor, -1)
          if line[0][0]==line[1][0]:
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
          
      def calculateBarLength(self,i):
          barLength=int(round((self.dotsGap-2*self.dotRadius)*i))
          if barLength<0:
            barLength=0
          elif barLength>self.dotsGap-2*self.dotRadius-2:
            barLength=self.dotsGap-2*self.dotRadius-2
          return barLength
          
      #called internally
      def drawHorizontalProgressLine(self,line,color,i):
          startingDotPos=self.dotPosList[line[0][0]][line[0][1]]
          barLength=self.calculateBarLength(i)
          lineTopLeftPos=(startingDotPos[0]+self.dotRadius+1,startingDotPos[1]-self.dotRadius)
          lineBottomRightPos=(lineTopLeftPos[0]+barLength,lineTopLeftPos[1]+2*self.dotRadius)
          cv2.rectangle(self.grid, lineTopLeftPos, lineBottomRightPos, self.currenLineColor, -1)
     
      #called internally
      def drawVerticalProgressLine(self,line,color,i):
          startingDotPos=self.dotPosList[line[0][0]][line[0][1]]
          barLength=self.calculateBarLength(i)
          lineTopLeftPos=(startingDotPos[0]-self.dotRadius,startingDotPos[1]+self.dotRadius+1)
          lineBottomRightPos=(lineTopLeftPos[0]+2*self.dotRadius,lineTopLeftPos[1]+barLength)
          cv2.rectangle(self.grid, lineTopLeftPos, lineBottomRightPos, self.currenLineColor, -1)
     
      
      
      #called internally
      def drawProgressBarOverLastSelectedLine(self,i):
         line=self.lastSelectedLine
         if line[0][0]==line[1][0]:
             self.drawHorizontalProgressLine(line,self.currenLineColor,i)
         else:
             self.drawVerticalProgressLine(line,self.currenLineColor,i)
         self.progress_bar_drawn_over_line=line
      
      def removeProgressBar(self):
          line=self.progress_bar_drawn_over_line
          if line==None:
             return
          if line[0][0]==line[1][0]:
             self.drawHorizontalLine(line,(0,0,0))
          else:
             self.drawVerticalLine(line,(0,0,0))
      
      #not fully implemented      
      def blinkTester(self):
         oldline=[(0,0),(0,1)]
         i=0
         maxiteration=1000
         while True:
            line=self.findSelectedLine(87,20)
            if line==None:
               i=0
               continue
            if line!=oldline:
               # or line==alreadySElectedLIne()
               self.removeProgressBarOverLastSelectedLine()
               i=0
               oldline=line
               continue
            if i<maxiteration:
               i+=1
            self.drawProgressBarOverLastSelectedLine(i/float(maxiteration-1))
            self.displayGrid()
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
               cv2.destroyWindow("grid window")
               break
            
         
if __name__=="__main__":
   cv2.namedWindow("grid window", cv2.WINDOW_NORMAL)
   grid =Grid(4,4,8,80,dottype=1)
   grid.drawLine(((1,1),(2,1)))
   grid.drawLine(((0,0),(1,0)))
   grid.drawLine(((0,1),(1,1)))
   grid.drawLine(((2,1),(2,2)))
   grid.drawLine(((3,1),(3,2)))
   grid.drawBox((2,1),boxcolor=0)
   grid.drawBox((1,2),boxcolor=1)   
   grid.blinkTester()
   cv2.namedWindow("grid window", cv2.WINDOW_NORMAL)   
   grid.displayGrid()
   key = cv2.waitKey() & 0xFF
   if key == 27:
     cv2.destroyWindow("grid window")
     
    

