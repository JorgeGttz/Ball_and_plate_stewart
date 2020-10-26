#Test of libirary to move platafor 6DOF

#----Plataform information----#
base_length = 92
servo_links = [16.46,117.22]
scrapt = 6
centroid_dist = 72.91



min_servo_signal = [0,36,0,64,0,65]
max_servo_signal = [108,150,106,180,104,180]

min_signal_degree = [7,53,7,85,5,77]
max_signal_degree = [97,140,95,175,90,157]

pca_channels = [0,1,2,8,9,10]

from board import SCL, SDA
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from camera_v2 import ball_info
import threading
import matplotlib.pyplot as plt
import cv2
import time as t

i2c= busio.I2C(SCL,SDA)
pca= PCA9685(i2c)

pca.frequency = 50

a=800       #Pulso minimo
b=2700      #Pulso maximo

home_degree = [75,72,75,100,70,85]       #angulos para home

servos=[]

for i in range(6):
    servos.append(servo.Servo(pca.channels[pca_channels[i]], min_pulse=a, max_pulse=b)) 
    servos[i].angle = home_degree[i]
    t.sleep(0.5)

import borra_functions as bf
import numpy as np
import math
from time import sleep

base_points = bf.base_points(base_length)

angles = [0.0,0.0,0.0]
translation = [0,0,110]

print("Done ...")
sleep(0.5)

#Ticker
class ticker(object):
    def __init__(self,initial = 0, update_interval = 0.001):
        self.ticker = initial
        self.update_interval = update_interval
    
    def init(self):
        self.ticker += 1
        threading.Timer(self.update_interval, self.init).start()

integration_time=ticker()
integration_time.init()

#Update camera
ball=ball_info("verde")         
    
#-----Plotting PID-----#
time=200
def plotting():
    global ax
    fig,ax = plt.subplots(2)
    fig.suptitle("PID Controller")
    ax[0].set_title("X position")
    ax[1].set_title("Y position")
    ax[1].set(xlabel="Time(ms) x30", ylabel="Position")
    ax[0].set(xlabel="", ylabel="Position")
    for i in range(2):
        ax[i].set_ylim(-300,300)
        ax[i].grid()
    

#cicle set_point
def set_circle(x,side):
    radio=100
    y=math.sqrt(math.pow(100,2) - math.pow(x,2))
    if side == "down":  y = y*-1    
    return y

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
        
        end_servo = bf.set_servo_values(servos_value,min_signal_degree,max_signal_degree,min_servo_signal,max_servo_signal,"online",servos)
    
           
    except ValueError:
        print("\n\x1b[1;31m"+"Error: It isn't posible set the current position (MathDomain Error)\n")
        print("\x1b[0;37m",end="")

set_plataform([0,0,0],[0,0,110])
t.sleep(1)
set_plataform([0,0,0],[0,0,114])


def PID_control():
    #PID setting
    DIV_KP=200
    DIV_KI=1000
    DIV_KD=50
    area_x=0
    area_y=0
    error_anterior_x=0
    error_anterior_y=0
    positions_x=[0,-150,100,100,-150,-150]  #set points x
    positions_y=[0,100,100,-90,-100,100]    #set points y   
    change_set_point=0
    xy_label=[]
    yy_label=[]
    x_label=[]
    list_point_x=[]
    list_point_y=[]

    while True:
        for i in range(time):

            ball.update_position()
            x_position=ball.position.x
            y_position=ball.position.y
            ball_on_plate=ball.position.ball_on_plate
    
            Kp=1.55
            Ki=0.22
            Kd=18
    
            #set_point_x=positions_x[change_set_point]
            #set_point_y=positions_y[change_set_point]
                
            if i<(time/2):
                side="up"
            if i>=(time/2): 
                side="down"
                i = time - i
            
            #set_point_x = (time/2) - abs(i*2)
            #set_point_y = set_circle((time/2) - abs(i*2), side)
            
            set_point_x = 0
            set_point_y = 0     
    
            error_x = set_point_x - x_position
            error_y = set_point_y - y_position
    
            if(integration_time.ticker > 1):
                area_x=(error_x/DIV_KI)+area_x
                area_y=(error_y/DIV_KI)+area_y
                if(area_x > 5): area_x=5
                if(area_y > 5):   area_y=5
                if(area_x < -5):   area_x=-5
                if(area_y < -5):   area_y=-5
                integration_time.ticker = 0
    
            derivate_x=(error_x - error_anterior_x)/DIV_KD
            derivate_y=(error_y - error_anterior_y)/DIV_KD
    
            controller_px = (Kp*error_x/DIV_KP)
            controller_ix = (Ki*area_x)
            controller_dx = derivate_x*Kd
            controller_py = (Kp*error_y/DIV_KP) 
            controller_iy = (Ki*area_y)
            controller_dy = derivate_y*Kd
    
            pitch = controller_px + controller_ix + controller_dx
            roll = controller_py + controller_iy + controller_dy
    
            if(pitch >= 6.5):   pitch=6.5
            if(pitch <= -6.5):  pitch=-6.5
            if(roll >= 6.5):    roll=6.5
            if(roll <= -6.5):   roll=-6.5
    
            x_plataform=pitch       
            y_plataform=-roll
    
            if(ball_on_plate == True):
                set_plataform([0,-pitch,roll],[x_plataform,y_plataform,117])
            else:
                set_plataform([0,0,0],[0,0,117])
                area_x=0
                area_y=0
    
            error_anterior_x = error_x
            error_anterior_y = error_y
    
            #print("X={}, Y={}, area_x={}, pitch={}".format(x_position,y_position,area_x,pitch))
            
        
            xy_label=np.append(xy_label,x_position)
            yy_label=np.append(yy_label,y_position)
            x_label=np.append(x_label,i)
            list_point_x=np.append(list_point_x,set_point_x)
            list_point_y=np.append(list_point_y,set_point_y)
        
        #plotting() 
        #ax[0].plot(x_label,xy_label,"b",label="x position")
        #ax[0].plot(x_label,list_point_x,"r--",label="set point")
        #ax[1].plot(x_label,yy_label,"g",label="y position")
        #ax[1].plot(x_label,list_point_y,"r--",label="set point")
        #ax[0].legend(loc="upper right")
        #ax[1].legend(loc="upper right")
        #plt.show()
    
        #set points change
        change_set_point += 1
        if change_set_point > 5 : change_set_point=0
    
        yy_label=[]
        xy_label=[]
        x_label=[]
        list_point_x=[]
        list_point_y=[]

def main():
    rc=0
    try:
        PID_control()
    except KeyboardInterrupt:
        print("Closing program")   
    finally:
        #running=False
        cv2.destroyAllWindows()
    return rc

if __name__== "__main__":
    exit(main())
