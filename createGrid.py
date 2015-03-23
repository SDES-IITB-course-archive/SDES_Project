import numpy as np
import cv2



class Grid(object):
      def __init__(self,row=4,col=4,dotRad=4,dotsGap=20,dottype=0,color=(255,0,0)):   #dotsGap includes dotRad
          self.row=row
          self.col=col
          self.dotRad=dotRad
          self.dotsGap=dotsGap
          self.dottype=dottype
          self.color=color
          self.height=(row-1)*dotsGap+2*dotRad
          self.width=(col-1)*dotsGap+2*dotRad
          self.grid=np.zeros((self.width,self.height,3),np.uint8)
          self.dotPosList=[]
          self.fillGrid()
          
          
      def fillGrid(self):
          y=self.dotRad
          while y<self.width:
            x=self.dotRad
            while x<self.height:
              if self.dottype==0:
                 cv2.circle(self.grid,(x,y), self.dotRad, self.color, -1)
              else:
                 cv2.rectangle(self.grid,(x-self.dotRad,y-self.dotRad),(x+self.dotRad,y+self.dotRad), self.color, -1)
              self.dotPosList.append([x,y])
              x+=self.dotsGap
            y+=self.dotsGap
     
      def displayGrid(self):
          cv2.imshow("grid window",self.grid)
          
if __name__=="__main__":
   grid =Grid(6,8,8,40)
   grid.displayGrid()
   key = cv2.waitKey()
   if key == 27:
     cv2.destroyWindow("grid window")
    

