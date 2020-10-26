from board import SCL, SDA
import busio
from time import sleep

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import time 

def init():
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)

    pca.frequency = 50

    a=800		#Pulso minimo
    b=2700		#Pulso maximo
    pca_channels=[0,1,2,3,4,5,15]
    home_degree = [140,30,140,50,150,60]
    global servos
    servos=[]
    for i in range(7):
        servos.append(servo.Servo(pca.channels[pca_channels[i]], min_pulse=a, max_pulse=b))
        # servos[i].angle = home_degree[i]
        #sleep(0.2)
        # servos[1].angle=90

def set_servo(numero,angulo):
    servos[numero].angle=angulo

init()
set_servo(6,90)
