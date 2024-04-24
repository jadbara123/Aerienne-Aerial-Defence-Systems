import cv2 as cv
import numpy as np


videoCapture = cv.VideoCapture(0)


params = cv.SimpleBlobDetector_Params()

params.filterByArea = True
params.minArea = 100  
params.maxArea = 5000  

params.filterByCircularity = True
params.minCircularity = 0.7


params.filterByInertia = False
params.minInertiaRatio = 0.5

params.filterByConvexity = False
params.minConvexity = 0.5


detector = cv.SimpleBlobDetector_create(params)

while True:
    ret, frame = videoCapture.read()
    if not ret:
        break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

 
    keypoints = detector.detect(grayFrame)

    for keypoint in keypoints:
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])
        size = int(keypoint.size)
        
     
        cv.circle(frame, (x, y), size, (0, 255, 255), 2)
        
       
        cv.circle(frame, (x, y), 5, (0, 0, 255), -1)

    cv.imshow("circles", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()