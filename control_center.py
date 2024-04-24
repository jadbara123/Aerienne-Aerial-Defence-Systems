import cv2, os
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

coordinete_file = ''
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

def konuma_git(inputx, inputy):
    move_alt_stepper(inputx)
    move_ust_stepper(inputy)

def take_latest_message(file):
    file_dir =  os.listdir(file)
    sorted_file = []
    for i in file_dir:
        i = i.split(".txt")
        sorted_file.append(int(i[0]))
    with open(file+"/"+str(max(sorted_file))+".txt", "r") as f:
        content = f.read()
        content_list = content.split(",")
        f.close()
    return content_list[0], content_list[-1]
while 1:
    errorx, errory = take_latest_message(coordinete_file)
    if errorx is not None:
        dd = prev_ex - errorx
        if -5 < dd < 5:
            olcumx = int(prev_ex)
        dd = prev_ey - errory
        if -5 < dd < 5:
            olcumy = int(prev_ey)
        konuma_git(errorx, errory)
        prev_ex = errorx
        prev_ey = errory
    else:
        pass
