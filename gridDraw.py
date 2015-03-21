import cv2
from numpy import *


mat = zeros((16,16,3),uint8)

width, height,_ = mat.shape

dist=4
i=0
while i<height:
  cv2.line(mat,(0,i),(width,i),(255,255,255))
  i+=dist

i=0
while i<width:
  cv2.line(mat,(i,0),(i,height),(255,255,255),4)
  i+=dist


i=0
while i<width:
   j=0
   while j<height:
     mat[i][j] = 10
     j+=dist
   i+=dist




while True:
  cv2.imshow("1",mat)
  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow("1")
    break


