import cv2
import createGrid
cam = cv2.VideoCapture(0)


cv2.namedWindow("Webcam_images", cv2.WINDOW_NORMAL)
_,img = cam.read()

grid=createGrid.Grid(6,6)

def blendGrid(img1,img2,x=210,y=360):
    if img1==None:
       return
    rows,cols,channels = img2.shape
    roi = img1[x:x+rows, y:y+cols ]

    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask)

    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg,img2_fg)
    img1[x:x+rows, y:y+cols ] = dst




while 1:
  _,img = cam.read()
  img=cv2.flip(img, flipCode=1)
  blendGrid(img,grid.grid)
  cv2.imshow("Webcam_images",img)
  k=cv2.waitKey(1)
  if k==27:
   cv2.destroyWindow("Webcam_images")
   cam.release()

 
   


   
