import RPi.GPIO as GPIO
import time
import os

push=23

cont=0

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(push,GPIO.IN,GPIO.PUD_UP) #configuracion de entrada

#callback

def Cuenta(channel):
    global cont
    cont += 1
    os.system("clear")
    print("Contador: ",cont)
    time.sleep(0.1)   

#interrupciones
GPIO.add_event_detect(push, GPIO.RISING, callback = Cuenta)


print("Contador : ", cont)

#bucle principal

while(cont < 5):
    pass


