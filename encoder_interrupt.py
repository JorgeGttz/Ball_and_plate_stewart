from RPi import GPIO
from time import sleep

clk = 27
dt = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clkLastState = GPIO.input(clk)

def my_callback(channel):  
    global clkLastState
    global counter
   
    clkState = GPIO.input(clk)
    if clkState != clkLastState:
        dtState = GPIO.input(dt)
        if dtState != clkState:
            counter += 1
        else:
            counter -= 1
        print(counter)
    clkLastState = clkState
    #sleep(0.01)
  


counter = 0
clkLastState = GPIO.input(clk)
GPIO.add_event_detect(clk, GPIO.FALLING  , callback=my_callback, bouncetime=40)

while counter<10:
    pass
  
GPIO.cleanup()


