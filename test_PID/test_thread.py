import threading
from time import sleep

x=0
y=0
ball_on_plate=False

def funtion(arg):
	global runing
	global x,y,ball_on_plate
	runing=True
	while runing:
		x+=1
		y+=1
		ball_on_plate = not ball_on_plate
		sleep(0.6)
		

thread1 = threading.Thread(target=funtion,args=(1,))
print("Inicio de codigo")
thread1.start()	

while True:
	try:
		print("X={}, Y={}, Plate={}".format(x,y,ball_on_plate))
		sleep(0.2)
	except KeyboardInterrupt:
		print("Exit")
		runing=False
		break



	

runing=False
