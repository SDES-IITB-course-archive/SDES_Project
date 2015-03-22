import cv2
import createGrid
cam = cv2.VideoCapture(0)

screen_res = 1280, 720
scale_width = screen_res[0] / cam.read()[1].shape[1]
scale_height = screen_res[1] / cam.read()[1].shape[0]
scale = min(scale_width, scale_height)
window_width = int(cam.read()[1].shape[1] * scale)
window_height = int(cam.read()[1].shape[0] * scale)
cv2.namedWindow("Webcam images", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Webcam images", window_width, window_height)
img = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

grid=createGrid.Grid()


while 1:
  img = cv2.cvtColor(cam.read()[1],cv2.COLOR_BGR2GRAY)
  cv2.imshow("Webcam images",img)
  


k=cv2.waitKey()
if k==27:
   cv2.destroyWindow("Webcam images")
   cam.release()

   
