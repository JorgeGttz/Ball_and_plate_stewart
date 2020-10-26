from board import SCL, SDA
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import time as t

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)

pca.frequency = 50

a=800		#Pulso minimo
b=2700		#Pulso maximo

ser0 = servo.Servo(pca.channels[ 0], min_pulse=a, max_pulse=b) #Servomotor MG995
ser1 = servo.Servo(pca.channels[ 1], min_pulse=a, max_pulse=b)
ser2 = servo.Servo(pca.channels[ 4], min_pulse=a, max_pulse=b)
ser3 = servo.Servo(pca.channels[ 5], min_pulse=a, max_pulse=b)
ser4 = servo.Servo(pca.channels[ 6], min_pulse=a, max_pulse=b)
ser5 = servo.Servo(pca.channels[ 7], min_pulse=a, max_pulse=b)

m=180
p1=135
p2=170
p3=90
ser0.angle = p3
t.sleep(0.5)
ser1.angle = m - p3
t.sleep(0.5)
ser2.angle = p1
t.sleep(0.5)
ser3.angle = m - p3
t.sleep(0.5)
ser4.angle = p2
t.sleep(0.5)
ser5.angle = m - p1
t.sleep(0.5)

'''
while True:
	for i in range(90,180,2):
		ser0.angle = i
		t.sleep(0.05)
		ser1.angle = m - i
		t.sleep(0.05)
		ser2.angle = i
		t.sleep(0.05)
		ser3.angle = m - i
		t.sleep(0.05)
		ser4.angle = i
		t.sleep(0.05)
		ser5.angle = m - i 
		t.sleep(0.05)
	for i in range(180,90,2):
		ser0.angle = i
		t.sleep(0.05)
		ser1.angle = m - i
		t.sleep(0.05)
		ser2.angle = i
		t.sleep(0.05)
		ser3.angle = m - i
		t.sleep(0.05)
		ser4.angle = i
		t.sleep(0.05)
		ser5.angle = m - i
		t.sleep(0.05)
'''
