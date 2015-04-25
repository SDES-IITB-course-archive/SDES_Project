import numpy as np
import cv2



class Grid(object):
      def __init__(self,row=4,col=4,dotRadius=4,dotsGap=20,dottype=0,color=(255,0,0)):   #dotsGap includes dotRadius
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
          
          
      def filldots(self):
          y=self.dotRadius
          i=0
          while y<self.width:
            x=self.dotRadius
            self.dotPosList.append([])
            while x<self.height:
              if self.dottype==0:
                 cv2.circle(self.grid,(x,y), self.dotRadius, self.color, -1)
              else:
                 cv2.rectangle(self.grid,(x-self.dotRadius,y-self.dotRadius),(x+self.dotRadius,y+self.dotRadius), self.color, -1)
              self.dotPosList[i].append((x,y))
              x+=self.dotsGap
            y+=self.dotsGap
            i+=1
     
      def displayGrid(self):
          cv2.imshow("grid window",self.grid)
          
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
             return None
      
      def detectVerticalLine(self,x,y):
             j=0
             noPossibleLine=True
             while j<=self.col-1:
               if x>self.dotPosList[0][j][0]-self.dotRadius and x<self.dotPosList[0][j][0]+self.dotRadius:
                  noPossibleLine=False
                  break;
               j+=1
             if noPossibleLine==True:
                return 	None
             i=0
             while i<=self.col-2:
               if y>self.dotPosList[i][0][1]+self.dotRadius and y<self.dotPosList[i+1][0][1]-self.dotRadius:
                  return (i,j)
             return None
      
      def isOutsideArea(self,x,y):
           if y<=self.dotPosList[0][0][1]-self.dotRadius or y>=self.dotPosList[self.row-1][0][1]+self.dotRadius \
           or x<=self.dotPosList[0][0][0]-self.dotRadius or x>=self.dotPosList[0][self.col-1][0]+self.dotRadius:
             return True
           else:
             return False
             
      def lineSelected(self,x,y):
           if self.isOutsideArea(x,y):
              return None
           line=self.detectHorizontalLine(x,y)
           if line!=None:
              self.lastSelectedLine=[line,(line[0],line[1]+1)]
              return self.lastSelectedLine
           line=self.detectVerticalLine(x,y)
           if line!=None:
              self.lastSelectedLine=[line,(line[0]+1,line[1])]
              return self.lastSelectedLine
           return None
           
           
       #draws line between dot1 and dot2    
      def drawLine(self,dot1,dot2,color=(255,255,255)):
           print self.dotPosList[dot1[0]][dot1[1]], self.dotPosList[dot2[0]][dot2[1]]
           cv2.line(self.grid, self.dotPosList[dot1[0]][dot1[1]], self.dotPosList[dot2[0]][dot2[1]], color, thickness=int(1.5*self.dotRadius))
       
      def drawLastSelectedLine(self):
           self.drawLine(self.lastSelectedLine)
           
if __name__=="__main__":
   grid =Grid(6,6,8,40,dottype=1)
   print grid.dotPosList[0][0]
   grid.drawLine((1,1),(2,1))   
   grid.displayGrid()
   key = cv2.waitKey()
   if key == 27:
     cv2.destroyWindow("grid window")
    

