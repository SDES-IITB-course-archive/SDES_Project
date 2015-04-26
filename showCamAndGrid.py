import cv2
import Grid
cam = cv2.VideoCapture(0)

circledot=0
rectdot=1

cv2.namedWindow("Webcam_images", cv2.WINDOW_NORMAL)
_,img = cam.read()

grid=Grid.Grid(row=5,col=5,dotRadius=8,dotsGap=60,dottype=1,color=(46,266,250))
grid.drawLine(((1,1),(2,1)))
grid.drawLine(((2,1),(2,2)))
grid.drawLine(((4,1),(4,2)))      
grid.drawBox((2,1),boxcolor=0)
grid.drawBox((1,3),boxcolor=1)

def blendGrid(img1,img2,x=210,y=360):
    if img1==None:
       return
    rows,cols,channels = img2.shape
    roi = img1[x:x+rows, y:y+cols ]
    
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




while 1:
  _,img = cam.read()
  img=cv2.flip(img, flipCode=1)
  blendGrid(img,grid.grid,110,300)
  cv2.imshow("Webcam_images",img)
  k=cv2.waitKey(1) & 0xFF
  if k==27:
   cv2.destroyWindow("Webcam_images")
   cam.release()
   break

 
  
