import RPi.GPIO as GPIO
import os
from time import sleep

#pines del encoder
CLK=27
DT=22
counter=0

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK,GPIO.IN)
GPIO.setup(DT, GPIO.IN)

Laststate=GPIO.input(DT)

#encoder rotary position
while(counter<10):
    State=GPIO.input(DT)
    if State != Laststate:
        if GPIO.input(CLK) != State:
            counter += 0.5
        else:
            counter -= 0.5
   
        print("Position: ",counter)
        sleep(0.01)
    
 
    Laststate = State


