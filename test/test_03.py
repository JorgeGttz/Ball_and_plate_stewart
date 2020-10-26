import numpy as np
import cv2
from time import sleep
import serial,re

UPDATE_TIME = .25

arduino = serial.Serial('COM1',115200)

while 1:
    try:
        if arduino.inWaiting() > 0:
            text = arduino.readline()
            print(text)
    except KeyboardInterrupt:
        arduino.close()
        break
