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

# Set the initial state of the enable pin (LOW for enabled, HIGH for disabled)


# Set the initial state of the enable pin (LOW for enabled, HIGH for disabled)
GPIO.output(EnablePinalt, GPIO.LOW)

Kpx = 3.52844346135723
Kix = 5.97731777084012
Kdx = 0.50884263758566
Kpy = 1.52844346135723
Kiy = 5.97731777084012
Kdy = 0.510884263758566

camera = cv2.VideoCapture(0)
dists = []
prev_ex = 0
prev_ey = 0

def move_ust_stepper(speed_raw):
    # Set the direction pin
    if np.abs(speed_raw) > 70 :
        if speed_raw < 0:
            direction = GPIO.HIGH
        else:
            direction = GPIO.LOW
        speed = np.abs(1/speed_raw)
        GPIO.output(DirPinust, direction)
        # Move the motor
        print("+++"+str(speed))
        for _ in range(int(speed_raw*0.1)):
            GPIO.output(StepPinust, GPIO.HIGH)
            time.sleep(speed)
            GPIO.output(StepPinust, GPIO.LOW)
            time.sleep(speed)

def move_alt_stepper(speed_raw):
    # Set the direction pin
    if np.abs(speed_raw) > 20 :
        if speed_raw > 0:
            direction = GPIO.HIGH
        else:
            direction = GPIO.LOW

        speed = np.abs(1/speed_raw)*3
        GPIO.output(DirPinalt, direction)

        # Move the motor0
        for _ in range(int(0.1*speed_raw)):
            GPIO.output(StepPinalt, GPIO.HIGH)
            time.sleep(speed)
            GPIO.output(StepPinalt, GPIO.LOW)
            time.sleep(speed)

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
        Px = errorx
        Ix = (errorx+prev_ex)*0.5
        Dx = (errorx-prev_ex)/0.5
        Py = errory
        Iy = (errory+prev_ey)*0.5
        Dy = (errory-prev_ey)/0.5
        inputx = Kpx*Px+Kix*Ix+Kdx*Dx
        inputy = Kpy*Py+Kiy*Iy+Kdy*Dy
        prev_ex = errorx
        prev_ey = errory
        print(inputx)
        konuma_git(inputx, inputy)
        yeni_cx , yeni_cy = yer_hesapla(img)
        if yeni_cy != None:
            cy = yeni_cy
            cx = yeni_cx
        cv2.circle(img, (int(cx), int(cy)), 20, (255,255,255), -1)
        cv2.imshow("kare", img)
        cv2.waitKey(1)
    else:
        pass