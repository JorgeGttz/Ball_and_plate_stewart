#Script for ball and plate menu
#Script realized by Jorge Alberto Gutierrez Padilla
#email: jorge_gttz@hotmail.com
#This program is a comparation betwen two types of controllers
#The PID control parallel and PID control serie, both are classics system
#These controllers have advantage and disaventage, you should use it 
#the best for your project.
#"Never stop learning because life never stops teaching"

import lcd
import RPi.GPIO as GPIO
from time import sleep
import threading
from board import SCL, SDA
import busio
import matplotlib.pyplot as plt
import math
import os,re

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

#-----Librarys for adc and Stewart 6DOF----#
import adc, camera
import cv2
import borra_functions as bf
import numpy as np


#Data PID
DIV_KP=200
DIV_KI=1000
DIV_KD=50
area_x=0
area_y=0
error_anterior_x=0
error_anterior_y=0
positions_x=[0,-150,100,100,-150,-150,0]  #set points x
positions_y=[0,100,100,-90,-100,100,0]
change_set_point=0
Kp=1.55
Ki=0.22
Kd=18
position_plataform=["Center","Right/Up","Left/Up","Left/Down","Right/Down","Right/Up","Center","Circle"]

#PINOUT
logos=["tnm","itcg","addictronics"]
push=23
menu_location=0
OE = 25             #Pin for disable servo
CLK=27
DT=22
funtion=None       #funciones      

#-----Plataform information-----#
base_length = 92
servo_links = [16.46,117.22]
scrapt = 6
centroid_dist = 72.91

#-----Servos settings-----------#
min_servo_signal = [0,36,0,60,0,70]
max_servo_signal = [108,150,106,170,104,180]

min_signal_degree = [7,53,7,85,5,77]
max_signal_degree = [97,140,95,165,90,157]

pca_channels = [0,1,2,8,9,10]

try:
    i2c= busio.I2C(SCL,SDA)
    pca= PCA9685(i2c)
except:
    print("Fail PCA9685 servos module")

pca.frequency = 50

a=800       #Pulso minimo
b=2700      #Pulso maximo

home_degree = [75,82,75,100,70,85]       #angulos para home

servos=[]

for i in range(6):
    servos.append(servo.Servo(pca.channels[pca_channels[i]], min_pulse=a, max_pulse=b))
    servos[i].angle = home_degree[i]
    sleep(0.5)

#----Plotting PID----#
time_plot=200
show_plot=False
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

#-----Circle set_point----#
def set_circle(x,side):
    radio=100
    y=math.sqrt(math.pow(100,2) - math.pow(x,2))
    if side == "down":  
        y=-y
    return y

#----Setup Plataform----#
base_points = bf.base_points(base_length)
angles = [0.0,0.0,0.0]
translation = [0,0,110]
print("Done ...")
sleep(0.5)

def set_plataform(angles,translation):  #([yaw,pitch,roll],[x,y,z])
    plate_points = bf.plate_points(centroid_dist,scrapt,angles,translation)

    try:
        theta1,theta2 = bf.get_servo_angle(plate_points,servo_links,base_points)
        servos_value = []
        for i in theta1:
            servos_value.append(int(i[0]))

        #-------Set angles servos------#
        end_servo = bf.set_servo_values(servos_value,min_signal_degree,max_signal_degree,min_servo_signal,max_servo_signal,"online",servos)
    
    except ValueError:
        print("\n\x1b[1;31m"+"Error: It isn't posible set the current position (MathDomain Error)\n")
        print("\x1b[0;37m",end="")

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(push,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(CLK,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(OE,GPIO.OUT)

Laststate = GPIO.input(CLK)
counter=0
menu=0

#---Init plataform---#
try:
    camera.init()
except:
    print("Fail camera module")
GPIO.output(OE,False)   #enable servos
set_plataform([0,0,0],[0,0,110])
sleep(1)
set_plataform([0,0,0],[0,0,114])


#Ticker
class ticker(object):
    def __init__(self, initial = 0, update_interval = 0.001):
        self.ticker = initial
        self.update_interval = update_interval

    def init(self):
        self.ticker += 1
        # Timer only runs once so call recursively in inc()
        threading.Timer(self.update_interval, self.init).start()

integration_time=ticker()
integration_time.init()

#callback
def count(channel):
    global menu
    global counter
    global funtion
    global show_plot
    
    if funtion ==15 or funtion==16 or funtion==17:
        funtion = None
        counter = 3        
    if funtion ==9 or funtion==10 or funtion==11:
        funtion = None
        counter = 3        
    
    if funtion == 14:               
        funtion = None
        counter = 2     
    
    for i in range(3):
        if funtion==9+i:    
            funtion = None    

    if funtion== 5:
        funtion = None
        counter = 3        

    for i in range(3):
        if menu ==6 and counter == i:   funtion=9+i   #Setup PID serie
    for i in range(3):
        if menu ==7 and counter == i:   funtion=15+i   #Setup PID serie
                                
    if menu ==5 and counter == 0:   funtion=14    #show funtions
    if menu ==4 and counter == 3:   menu = 3    #back
    #if menu ==2 and counter == 0:   menu=4      #pitch,roll, picth & roll
    if menu ==2 and counter == 1:   
        menu=5      #Show (show,Plotting)
        counter=0
    if menu ==2 and counter == 2:   funtion=4   #Altura
    if menu ==3 and counter == 0:   menu = 6    #Setup PID serie
    if menu ==3 and counter == 1:   menu = 7    #Setup PID parallel
    if menu ==3 and counter == 2:   funtion=5   #Conenct to pc

    if menu ==5 and counter == 1:   menu=8        

    for i in range(3):
        if menu ==4 and counter == i:   funtion=6+i #pitch,roll,pitch & roll
        if menu ==1 and counter == i:
            funtion=i+1                           #serie,paralel,game
        if menu ==0 and counter == i:   menu=1+i    #Control,prepare,setup    

    if (menu ==3 or menu==1 or menu==2) and counter == 3:   
        menu = 0    #back 
        counter=0        
    if menu ==1 and counter == 0:
        funtion=None
    if menu ==2 and counter == 0:       
        menu=4      #pitch,roll, picth & roll
        funtion=None

    if menu ==5 and counter == 3:   menu = 2     #back
    for i in range(2):
        if menu ==7-i and counter == 3:   menu=3      #back
        
    if counter == 3 and menu == 0:
        funtion=18
    if menu ==8 and counter == 3:   
        show_plot=False
        menu=5
    if menu ==8 and counter == 2:   
        show_plot=True
        menu=5
    
    counter=0
     
    print("Menu={}, Counter={}, Funtion={}, Plot={}".format(menu,counter,funtion,show_plot))

#digital_encoder_interrupt
def encoder(channel):
    global Laststate
    global counter
    global menu
    State=GPIO.input(CLK)
    if State != Laststate:
        dtState = GPIO.input(DT)
        if dtState != State:
            counter += 1
        else:
            counter -= 1
        #print("Position: ",counter)
    
      #sleep(0.01)
    if counter >=3: counter=3
    if counter <=0: counter=0
   
    Laststate = State
   

#interruptions
GPIO.add_event_detect(push, GPIO.RISING, callback = count, bouncetime=300)
GPIO.add_event_detect(CLK, GPIO.FALLING , callback = encoder,bouncetime=40)

#menu and funtions
def joystick():
    try:
        joystick_y = adc.read(1)
        joystick_x = adc.read(2)
    except:
        print("Fail PCF8591 adc module")
    
    if(joystick_x <= 120):  pitch = (joystick_x - 120)/120.0*-6.5
    elif (joystick_x >= 140):  pitch = (joystick_x - 140)/115.0*-6.5
    else:   pitch = 0

    if(joystick_y <= 120):  roll = (joystick_y - 120)/120.0*-6.5
    elif(joystick_y >= 140):  roll = (joystick_y - 140)/115.0*-6.5
    else:   roll = 0
    values=(pitch,roll)
    return values

#Get-ip
def get_ip():
    direction = os.popen("hostname -I").read().split(' ')
    direction=direction[0]
    ipv4_pattern=re.compile("^(\d{1,3}\.){3}\d{1,3}$")
   
    if ipv4_pattern.match(direction):
        print("IP match")
        ip=direction
    else:
        print("IP no match")
        ip=None
    return ip

def battery():
    try:
        value_adc=adc.read(3)
        sleep(0.01)
    except ValueError:
        print("Error adc module, voltage Battery")
    except:
        print("Error PCF8591 adc module")
    return value_adc
    

def setup(menu_insert):
    global menu
    global counter
    global funtion 
    global Kp
    global Ki
    global Kd
    global change_set_point
    #Values for plotting
    xy_label=[]
    yy_label=[]
    x_label=[]
    list_point_x=[]
    list_point_y=[]
    
    #baterry
    get_voltaje=battery()
    #print(get_voltaje)
    while get_voltaje < 180:    #Value for low voltage
        get_voltaje=battery()
        lcd.message("     Low Battery","      Recharge")
   
    #Setup menu in OLED display
    if(menu==0):
        lcd.write("Control","Prepare","Setup","OFF",True,counter)
    elif(menu==1):#Control
        lcd.write("PID serie","PID parallel","GAME","Back",True,counter)    
        
    elif(menu==2):#Prepare
        lcd.write("Pitch, Roll","Show","Height","Back",True,counter) 

    elif(menu==3):#Setup
        lcd.write("Set PID S","Set PID P","Conection PC","Back ",True,counter)
   
    elif(menu==4):#Pitch and roll
        lcd.write("Pitch(y)","Roll(x)","Pitch & Roll","Back ",True,counter)

    elif(menu==5):#show
        lcd.write("Show camera","Plotting","","Back",True,counter)

    elif(menu==6):  #setup PID serie
        lcd.write("Proportional","Integral","Derivative","Back ",True,counter)
    
    elif(menu==7):  #setup PID parallel
        lcd.write("Proportional","Integral","Derivative","Back ",True,counter)
    
    elif(menu==8):  #show plot (yes/no)
        lcd.write("",""," Yes"," No ",True,counter)
    
    if funtion == 1:
        lcd.message("            PID","           Serie")    
    if funtion == 2:
        lcd.message("            PID","         Paralell")         
    while funtion == 3:     #GAMe
        lcd.write("   Put the ball","  on the center","  with joystick","",False,counter)
        
        values=camera.position(show=False)  #get position (x,y and ball on plate)
        ball_on_plate=values[2]
        if ball_on_plate == True:
            for i in range(3):
                lcd.message("         Ready?","             "+str(3-i))
                sleep(1)
            lcd.message("           Go!","")
            while ball_on_plate == True:
                position=joystick()
                pitch=position[0]
                roll=position[1]
                values=camera.position(show=False)
                x_position=values[0]
                y_position=values[1]
                ball_on_plate=values[2]
                if x_position<=10 and x_position>=-10 and y_position<=10 and y_position>=-10:
                    lcd.message("        Winner!","          :)")
                    
                set_plataform([0,pitch,roll],[0,0,117])
            
            if ball_on_plate == False:
                lcd.message("        Looser!","          :(")
                sleep(3)

#main funtions(case)
    while funtion==1 or funtion ==2:   #Control PID Paralell and serial
        for i in range(time_plot):
            global area_x
            global area_y
            global error_anterior_x
            global error_anterior_y
            
            values=camera.position(show=False)  #get position (x,y and ball on plate)
            x_position=values[0]
            y_position=values[1]
            ball_on_plate=values[2]

            value_joystick = joystick()
            value_change = value_joystick[0]

            if value_change>=6.5:  
                change_set_point=change_set_point+1
                sleep(0.1)
                if change_set_point>=7: change_set_point=7
                print("Set point :"+position_plataform[change_set_point])
            if value_change<=-6.5:  
                change_set_point=change_set_point-1
                sleep(0.1)
                if change_set_point<0:  change_set_point=0
                print("Set point :"+position_plataform[change_set_point])   

            if(funtion==1):  #Gain PID serie
                Kp=1
                Ki=0
                Kd=0

            if(funtion==2):  #Gain PID parallel
                Kp=1.55
                Ki=0.22
                Kd=18

            
            if change_set_point<=6:
                set_point_x=positions_x[change_set_point]
                set_point_y=positions_y[change_set_point]
            
            if change_set_point==7:
                if show_plot == False:
                    if i<(time_plot/2):
                        side="up"
                    if i>=(time_plot/2):
                        side="down"
                        i = time_plot - i            
                    set_point_x = (time_plot/2) - abs(i*2)
                    set_point_y = set_circle((time_plot/2) - abs(i*2),side)
                else:
                    print("Turn off plotting, please")

            #set_point_x=0
            #set_point_y=0

            error_x = set_point_x - x_position    # x position error
            error_y = set_point_y - y_position    # y position error
            
            if(integration_time.ticker > 1): #Integrative time
                area_x=(error_x/DIV_KI)+area_x
                area_y=(error_y/DIV_KI)+area_y
                if(area_x > 5):   area_x=5
                if(area_y > 5):   area_y=5
                if(area_x < -5):   area_x=-5
                if(area_y < -5):   area_y=-5
                integration_time.ticker = 0
                
            derivate_x=(error_x - error_anterior_x)/DIV_KD
            derivate_y=(error_y - error_anterior_y)/DIV_KD

            controller_px=(Kp*error_x/DIV_KP)          
            controller_ix=(Ki*area_x)
            controller_dx=derivate_x*Kd
            controller_py=(Kp*error_y/DIV_KP)
            controller_iy=(Ki*area_y)
            controller_dy=derivate_y*Kd

            if(funtion==1):     #PID serie algorithm
                pitch = controller_px*(controller_ix + 1)*(controller_dx + 1)
                roll  = controller_py*(controller_iy + 1)*(controller_dy + 1) 

            if(funtion==2):     #PID paralell algorithm
                pitch = controller_px + controller_ix + controller_dx
                roll  = controller_py + controller_iy + controller_dy        


            if(pitch >= 6.5):     pitch=6.5
            if(pitch <= -6.5):   pitch=-6.5
            if(roll >= 6.5):    roll=6.5
            if(roll <= -6.5):   roll=-6.5
            
            x_platform=pitch
            y_platform=-roll
    
            if(ball_on_plate == True):  #ball must be on plate
                set_plataform([0,-pitch,roll],[x_platform,y_platform,117])
                print("X={}, Y={},".format(x_position,y_position))
            else:
                set_plataform([0,0,0],[0,0,117])
                area_x=0
                area_y=0
                
            #print("X={}, Y={}, area_x{}, pitch{}".format(x_position,y_position,area_x,pitch))
            #lcd.message("   X = {}".format(x_position),"   Y = {}".format(y_position))
            menu=0
            
            error_anterior_x = error_x
            error_anterior_y = error_y
            
            if show_plot:
                xy_label=np.append(xy_label,x_position)
                yy_label=np.append(yy_label,y_position)
                x_label=np.append(x_label,i)
                list_point_x=np.append(list_point_x,set_point_x)
                list_point_y=np.append(list_point_y,set_point_y)

            
        if show_plot:
            plotting() 
            ax[0].plot(x_label,xy_label,"b",label="x position")
            ax[0].plot(x_label,list_point_x,"r--",label="set point")
            ax[1].plot(x_label,yy_label,"g",label="y position")
            ax[1].plot(x_label,list_point_y,"r--",label="set point")
            ax[0].legend(loc="upper right")
            ax[1].legend(loc="upper right")
            plt.show()
                

            yy_label=[]
            xy_label=[]
            x_label=[]
            list_point_x=[]
            list_point_y=[]

    while funtion==4:   #Height
        position=joystick()
        height=position[1]
        set_plataform([0,0,0],[0,0,116+height])         
        lcd.message("         Height    ","Length:{:.2f}".format(116+height)+"mm")
        menu=2

    while funtion==5:   #IP direction
        ip_message=" Searching IP"
        for i in range(4):
            lcd.message(ip_message,"")
            ip_message+="."
            sleep(0.5)
        ip=get_ip()
        if ip is None:
            lcd.message("  IP not found","")
            sleep(2)
        while ip is not None and funtion==5:
            lcd.message("  IP Found:","  IP:{}".format(ip))        
            
    while(funtion ==6 or funtion == 7 or funtion == 8) :# move Pitch and roll 
        position=joystick()
        pitch=position[0]
        roll=position[1]
        if funtion==6:#Pitch
            set_plataform([0,pitch,0],[0,0,117])
            lcd.message("           Pitch    ","      Angle:{:.2f}".format(pitch)+"°")
        elif funtion==7:#Roll
            set_plataform([0,0,roll],[0,0,117])
            lcd.message("            Roll    ","      Angle:{:.2f}".format(roll)+"°")
        elif funtion==8:#Pitch and roll
            set_plataform([0,pitch,roll],[0,0,117])
            lcd.message("Pitch = {:.2f}".format(pitch)+"°","Roll = {:.2f}".format(roll)+"°")
        menu=2     

    while funtion==9 or funtion==10 or funtion==11:
        lcd.message("         Funtion","    no supported".format(Kp))

    counter_serial=0    #Gains for Kp,Ki,Kd
    while funtion==15 or funtion == 16 or funtion == 17:

        value_joystick = joystick()
        selector = value_joystick[1]
        if selector > 6:    counter_serial = counter_serial + 0.01
        elif selector < -6:   counter_serial = counter_serial - 0.01
        elif selector > -6 and selector < 6: counter_serial=counter_serial+0

        if funtion==15:
            Kp = Kp + counter_serial
            lcd.message("Proportional","     Kp={}".format(Kp)) 
            if Kp == 1.55:
                lcd.message("Proportional","     Kp={}".format(Kp) +"*Recom")
 
        if funtion==16:
            Ki = Ki + counter_serial
            lcd.message("Integral","     Ki={:.2f}".format(Ki)) 
            if Ki == 0.22:
                lcd.message("Integral","     Ki={}".format(Ki)+"*Recom")

        if funtion==17:
            Kd = Kd + counter_serial
            lcd.message("Derivative","     Kd={}".format(Kd)) 
            if Kd == 18:
                lcd.message("Derivative","     Kd={}".format(Kd)+"*Recom")
           
                     
    while funtion == 14:
        values=camera.position(show=True)
        lcd.message("       CAMERA","")
        menu=5

    while funtion == 18:
        os.system("exit")
        sleep(0.5)
        lcd.message("       Bye   Bye","          ;)")
        sleep(1)
        lcd.message("         Made by:","  Jorge Gutierrez")
        sleep(3)
        lcd.message("","")
        os.system("sudo init 0")   #Turn off raspberry
        
    
    cv2.destroyAllWindows()

#-------------Init code---------------#  
try:      
    lcd.init()
except:
    print("Fail display oled sh1106 module")
lcd.logo("raspi")
sleep(2)
lcd.message("         Stewart","  Plataform  6DOF")
sleep(2)
lcd.message("     BALL AND","         PLATE")
sleep(2)
for i in range(3):
    lcd.logo(logos[i])
    sleep(2)

def main():
    try:
        while True:
            setup(menu)
    except KeyboardInterrupt:
        print("Closing program")
    #except:
    #    print("Unexpected error :(")    
    finally:
        GPIO.cleanup()
        cv2.destroyAllWindows()

if __name__== "__main__":
    exit(main())
