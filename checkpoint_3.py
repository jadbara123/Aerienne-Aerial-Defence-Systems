import cv2, os
import numpy as np
import RPi.GPIO as GPIO
import time
import numpy as np
import math



MaxDelayust=0.001
MinDelayust=0.000001
MaxDelay=0.004
MinDelay = 0.000001
h= MaxDelay - MinDelay
hust = MaxDelayust- MinDelayust

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

coordinete_file = 'coordinate_file'
prev_ex = 0
prev_ey = 0

def move_ust_stepper(speed):
    # Set the direction pin
    if np.abs(speed) > 10 :
        if speed < 0:
            direction = GPIO.HIGH
        else:
            direction = GPIO.LOW
        speed = (90/480)*np.abs(speed)*(400/360)
        GPIO.output(DirPinust, direction)
        TotalSpin=int(speed/1.5)
        # Move the motor
        for CurrentSpin in range(int(speed/1.5)):
            k=(hust*TotalSpin)/2.39
            fx=(1/(2.50*TotalSpin/6))*math.exp((-(CurrentSpin-TotalSpin/2)**2)/(2*(TotalSpin/6)**2))*k #tahtadaki denklem
            delay=np.abs(-fx+MaxDelayust-MinDelayust)
            GPIO.output(StepPinust, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(StepPinust, GPIO.LOW)
            time.sleep(delay)

def move_alt_stepper(speed):
    # Set the direction pin
    if np.abs(speed) > 20 :
        if speed > 0:
            direction = GPIO.HIGH
        else:
            direction = GPIO.LOW

        speed = (100/640)*np.abs(speed)*(400/360)
        GPIO.output(DirPinalt, direction)
        TotalSpin=int(speed/2)
        # Move the motor0
        for CurrentSpin in range(int(speed/2)):
            k=(h*TotalSpin)/2.39
            fx=(1/(2.50*TotalSpin/6))*math.exp((-(CurrentSpin-TotalSpin/2)**2)/(2*(TotalSpin/6)**2))*k #tahtadaki denklem
            delay=np.abs(-fx+MaxDelay-MinDelay)
            GPIO.output(StepPinalt, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(StepPinalt, GPIO.LOW)
            time.sleep(delay)

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
    if errorx != '':
        errorx, errory = int(errorx), int(errory)
        dd = prev_ex - errorx
        if -5 < dd < 5:
            olcumx = 0
        else: olcumx = errorx
        dd = prev_ey - errory
        if -5 < dd < 5:
            olcumy = 0
        else: olcumy = errory
        konuma_git(olcumx, olcumy)
        prev_ex = errorx
        prev_ey = errory
    else:
        pass
