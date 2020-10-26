from gpiozero import LED,Button,AngularServo    #Import libraries for Button and Servo
from signal import pause       #Import libraries to pause the system

#Configurations for My servo_01 connected to pin 18 were
servo_01 = AngularServo(18,min_pulse_width = 0.0006,max_pulse_width = 0.0026,min_angle = 0,max_angle = 180)

#GPIO configurations
button_01,button_02 = Button(23),Button(24)
led_01,led_02 = LED(14),LED(15)
led_01.on()

def button_01_pressed():
    if servo_01.angle != 180:
        servo_01.angle+=10
        print("The servo_01 angle is {}".format(servo_01.angle))

        if servo_01.angle == 180:
            led_01.on()
        else:
            led_01.off()
            led_02.off()
    else:
        print("Servo_01 max position reached")
        
def button_02_pressed():
    if servo_01.angle != 0: 
        servo_01.angle-=10
        print("The servo_01 angle is {}".format(servo_01.angle))

        if servo_01.angle == 0:
            led_02.on()
        else:
            led_01.off()
            led_02.off()
    else:
        print("Servo_01 min position reached")
        
button_01.when_pressed = button_01_pressed
button_02.when_pressed = button_02_pressed

pause()
