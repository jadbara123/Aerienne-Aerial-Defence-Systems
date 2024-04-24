import cv2
cam = cv2.VideoCapture(0)

while 1:
    ret, kare = cam.read()
    kare = cv2.resize(kare, (640, 480))
    cv2.imshow("kare", kare)
    cv2.waitKey(1)