import cv2
import math
import numpy as np

def help():
    print """\nThis program demonstrates line finding with the Hough transform.\n"
         "Usage:\n"
         "./houghlines <image_name>, Default is pic1.jpg\n"""


def main(arg1, filename="/home/tanmoy/Downloads/Wallpapers/cup-of-hot-chocolate-24576.jpg"):
  
  srcimg = cv2.imread(filename)
 
   
  
  gray = cv2.cvtColor(srcimg,cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray,50,150,apertureSize = 3)

  if arg1==0:
    lines=cv2.HoughLines(edges, 1, np.pi/180, 200 )
    for rho,theta in lines[0]:
      a = np.cos(theta)
      b = np.sin(theta)
      x0 = a*rho
      y0 = b*rho
      x1 = int(x0 + 1000*(-b))
      y1 = int(y0 + 1000*(a))
      x2 = int(x0 - 1000*(-b))
      y2 = int(y0 - 1000*(a))
      cv2.line(srcimg,(x1,y1),(x2,y2),(0,0,255),2)
  
  elif arg1==1:
    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(srcimg,(x1,y1),(x2,y2),(0,255,0),2)
 
  cv2.imshow(filename, srcimg);
  #imshow("detected lines", cdst);

  

import glob
for frmt in [".bmp",".jpg",".png"]:
    for filename in glob.glob("/home/tanmoy/Downloads/Wallpapers/*"+frmt):
       main(0,filename)
       cv2.waitKey();
