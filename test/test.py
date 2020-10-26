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

pca_channels = [0,1,4,5,6,7]  
#min_signal_degree = [5,77,12,83,7,85]       ##Valor que se obtuvpo en 90-0-90-0-90-0
#max_signal_degree = [90,157,97,170,95,173]
#home_degree = [90,77,97,83,95,85]
home_degree = [5,157,12,170,7,173]
servos = []

for i in range(6):
	servos.append(servo.Servo(pca.channels[pca_channels[i]], min_pulse=a, max_pulse=b))
	servos[i].angle = home_degree[i]
	print("Setting servo {} to {} degree".format(i,home_degree[i]))
	t.sleep(1)
