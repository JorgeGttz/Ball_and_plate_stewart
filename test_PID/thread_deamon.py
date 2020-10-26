import threading
import logging
from time import sleep

def funcion():
	while True:
		print("ok")

def daemon():
    funcion()
	

for i in range(2):i
	d = threading.Thread(target=daemon, name='Daemon')
	d.setDaemon(True)
	d.start()

	d.join()	

	print("Ok")
