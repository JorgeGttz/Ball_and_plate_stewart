#obtener ip y movimientos del servo para conectar con otro ordenador

import re,os
from board import SCL,SDA
import busio
import time

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

def get_ip():
    direction= os.popen("hostname -I").read().split(' ')
    direction=direction[0]
    ipv4_pattern=re.compile("^(\d{1,3}\.){3}\d{1,3}$")

    if ipv4_pattern.match(direction):
        #print("Match")
        ip=direction
        #print(ip)
    else:
        #print("No Match")
        ip=None
    return ip

def servo_init():
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
 
    a=800       #Pulso minimo
    b=2700      #Pulso maximo
    pca_channels=[0,8,2,3,4,5,15]
    #home_degree = [140,30,140,50,150,60]
    global servos
    servos=[]
    for i in range(7):
        servos.append(servo.Servo(pca.channels[pca_channels[i]], min_pulse=a, max_pulse=b))
 
def set_servo(numero,angulo):
    servos[numero].angle=angulo
        
#servo_init()
#set_servo(6,50)
