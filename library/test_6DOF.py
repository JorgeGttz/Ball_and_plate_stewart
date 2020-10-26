#Test of libirary to move platafor 6DOF

#----Plataform information----#
base_length = 92
servo_links = [16.46,117.22]
scrapt = 6
centroid_dist = 72.91

min_servo_signal = [0,66,0,64,0,70]
max_servo_signal = [108,180,106,180,104,180]

min_signal_degree = [12,83,7,85,5,77]
max_signal_degree = [97,170,95,175,90,157]

pca_channels = [0,1,2,8,9,10]

from board import SCL, SDA
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import time as t
try:
    i2c= busio.I2C(SCL,SDA)
    pca= PCA9685(i2c)
except:
    print("Fail PCA 9586 module")

pca.frequency = 50

a=800       #Pulso minimo
b=2700      #Pulso maximo

home_degree = [75,82,75,100,70,85]       #angulos para home

servos=[]

for i in range(6):
    servos.append(servo.Servo(pca.channels[pca_channels[i]], min_pulse=a, max_pulse=b)) 
    servos[i].angle = home_degree[i]
    t.sleep(0.5)

import adc
import borra_functions as bf
import numpy as np
from time import sleep

base_points = bf.base_points(base_length)

angles = [0.0,0.0,0.0]
translation = [0,0,110]

print("Done ...")
sleep(0.5)

#bf.clear_screen()

#-----Rutine code -----#
#while True:
def set_plataform(angles,translation):  #([yaw,pitch,roll],[x,y,z])

    plate_points = bf.plate_points(centroid_dist,scrapt,angles,translation)
    
    try:
        theta1,theta2 = bf.get_servo_angle(plate_points,servo_links,base_points)
        #print("get_servo_angle")
        servos_value = []
        for i in theta1:
            servos_value.append(int(i[0]))
        
        print("{}Angles{}\nYaw = {} | Pitch = {} |Roll = {}".format("-"*15,"-"*15,str(angles[0]).rjust(3,' '),str(angles[1]).rjust(3,' '),str(angles[2]).rjust(3,' ')))
        print("{}Translation{}\nDx  = {} | Dy    ={} | Dz   = {}".format("-"*12,"-"*13,str(translation[0]).rjust(3,' '),str(translation[1]).rjust(3,' '),str(translation[2]).rjust(3,' ')))       
        
    #----Servos angles----#
        print("\n{}The servos value are{}\n".format("-"*11,"-"*12),end="")
        print("|",end="")
        for i in range(6):
            print(" ser{} |".format(i),end="")
        print("\n|",end="")
        for i in range(6):
            print(" {} |".format(str(servos_value[i   ]).rjust(4,' ')),end="")
    
        print("\n"+"-"*43+"\n")
    
    #----------Set angles servos----------#
        end_servo = bf.set_servo_values(servos_value,min_signal_degree,max_signal_degree,min_servo_signal,max_servo_signal,"online",servos)
    
           
    except ValueError:
        print("\n\x1b[1;31m"+"Error: It isn't posible set the current position (MathDomain Error)\n")
        print("\x1b[0;37m",end="")

set_plataform([0,0,0],[0,0,110])
t.sleep(1)
set_plataform([0,0,0],[0,0,114])

while True:
    joystick_y = adc.read(1)
    joystick_x = adc.read(2)    
    
    if(joystick_x <= 120):  pitch = (joystick_x - 120)/120.0*-6.5
    if(joystick_x >= 140):  pitch = (joystick_x - 140)/115.0*-6.5
    if(joystick_x > 120 and joystick_x < 140): pitch = 0
    if(joystick_y <= 120):  roll = (joystick_y - 120)/120.0*-6.5
    if(joystick_y >= 140):  roll = (joystick_y - 140)/115.0*-6.5
    if(joystick_y > 120 and joystick_y < 140): roll = 0
    
    set_plataform([0,pitch,roll],[0,0,117])
