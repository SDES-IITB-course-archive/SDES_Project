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
          
      
      def detectClosestNode(dotPosList,pos):             
          nodes = np.asarray(dotPosList)
          dist_2 = np.sum((nodes - pos)**2, axis=1)
          closestNode=np.argmin(dist_2)
          y=closestNode/self.col
          x=closestNode%self.row
          return (x,y)
          
      def detectLine(x,y):
          if y<self.dotPosList[0][0][1]-self.dotRadius or y>self.dotPosList[self.row][0][1]+self.dotRadius \
          or x<self.dotPosList[0][0][0]-self.dotRadius or x>self.dotPosList[0][self.col][0]+self.dotRadius:
             return -1
          else:
             y<self.dotPosList[0][0][1]+self.dotPosList:

if __name__=="__main__":
   grid =Grid(6,6,8,40)
   grid.displayGrid()
   print grid.dotPosList
   key = cv2.waitKey()
   if key == 27:
     cv2.destroyWindow("grid window")
    

