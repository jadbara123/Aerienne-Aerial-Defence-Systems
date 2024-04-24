import cv2
import numpy as np
cap = cv2.VideoCapture(0)

while 1:
   ret, img = cap.read()
   
   low  = (0,70,50)
   high = (10,255,255)   
   hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   filtered = cv2.inRange(hsv_image, low, high)
   kernel = np.ones((10, 10), np.uint8) 
   erosion = cv2.erode(filtered, kernel, 
                        iterations=1)
   # find contours in the binary image
   contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   cpX, cpY = 0, 0
   true_coords = []
   for c in contours:
      # calculate moments for each contour
      M = cv2.moments(c)
   
      # calculate x,y coordinate of center
      cX = int(M["m10"] / (M["m00"]+0.000000000001))
      cY = int(M["m01"] / (M["m00"]+0.000000000001))
      if not(abs(cpX-cX)<10 and abs(cpY- cY)<10):
         cX = cpX
         cY = cpY
      cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
      cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cpX = cX
      cpY = cY
   
      # display the image
   cv2.imshow("Image", img)
   cv2.imshow("Image1", erosion)
   cv2.waitKey(1)