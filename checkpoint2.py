import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import numpy as np

# Define GPIO pins connected to the stepper motor driver
EnablePinust = 17
StepPinust = 27
DirPinust = 22
EnablePinalt = 17
StepPinalt = 19
DirPinalt = 26

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
GPIO.setup(EnablePinust, GPIO.OUT)
GPIO.setup(StepPinust, GPIO.OUT)
GPIO.setup(DirPinust, GPIO.OUT)
GPIO.setup(EnablePinalt, GPIO.OUT)
GPIO.setup(StepPinalt, GPIO.OUT)
GPIO.setup(DirPinalt, GPIO.OUT)

camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(4,480)
dists = []
prev_ex = 0
prev_ey = 0

def move_ust_stepper(speed):
    # Set the direction pin
    if np.abs(speed) > 10 :
        if speed < 0:
            direction = GPIO.HIGH
        else:
            direction = GPIO.LOW
        speed = (100/240)*np.abs(speed)
        GPIO.output(DirPinust, direction)
        # Move the motor
        for _ in range(int(speed)):
            GPIO.output(StepPinust, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(StepPinust, GPIO.LOW)
            time.sleep(0.001)

def move_alt_stepper(speed):
    # Set the direction pin
    if np.abs(speed) > 20 :
        if speed > 0:
            direction = GPIO.HIGH
        else:
            direction = GPIO.LOW

        speed = (100/320)*np.abs(speed)
        GPIO.output(DirPinalt, direction)

        # Move the motor0
        for _ in range(int(speed)):
            GPIO.output(StepPinalt, GPIO.HIGH)
            time.sleep(0.003)
            GPIO.output(StepPinalt, GPIO.LOW)
            time.sleep(0.003)

def calculate_distance_between_points(point1, point2=[320, 240]):
    # Calculate Euclidean distance between two points
    distance = np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    return (point1[0] - point2[0]), (point1[1] - point2[1]), distance

def find_largest_contour_center(binary_image):
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None

    largest_contour = max(contours, key=cv2.contourArea)
    moments = cv2.moments(largest_contour)

    # Calculate the centroid of the largest contour
    cx = int(moments['m10'] / (moments['m00']+0.000000000000000004))
    cy = int(moments['m01'] / (moments['m00']+0.000000000000000004))

    return cx, cy

def mesafe_hesapla(image, point=[320,240]):
    cx, cy = yer_hesapla(image)
  
    if cx != None:  
        distx, disty, dist = calculate_distance_between_points([cx,cy], point)
        return distx, disty, dist
    else:
        return None, None, None
    
def yer_hesapla(image):
    low  = (0,70,50)
    high = (10,255,255)   
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    filtered = cv2.inRange(hsv_image, low, high)
    kernel = np.ones((10, 10), np.uint8) 

    # erode the image 
    erosion = cv2.erode(filtered, kernel, 
                        iterations=1) 
    cx, cy = find_largest_contour_center(erosion) 
    if cx != None:  
        return cx, cy
    else:
        return None, None
 
def konuma_git(inputx, inputy):
    move_alt_stepper(inputx)
    move_ust_stepper(inputy)
    
while 1:
    ret, img = camera.read()
    img = cv2.resize(img, (640,480))
    print(img)
    errorx, errory, _ = mesafe_hesapla(img)
    print(errory)
    if errorx != None:
        dd = prev_ex - errorx
        if -5 < dd < 5:
            olcumx = int(prev_ex)
        dd = prev_ey - errory
        if -5 < dd < 5:
            olcumy = int(prev_ey)
        
        konuma_git(errorx, errory)
        yeni_cx , yeni_cy = yer_hesapla(img)
        if yeni_cy != None:
            cy = yeni_cy
            cx = yeni_cx
        cv2.circle(img, (int(cx), int(cy)), 20, (255,255,255), -1)
        cv2.imshow("kare", img)
        cv2.waitKey(1)
    else:
        pass
