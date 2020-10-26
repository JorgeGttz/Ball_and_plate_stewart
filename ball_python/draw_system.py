import borra_functions as bf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import sleep
import importlib
###Create a new figure to graph  3D

#Draw base
base_points = bf.base_points(92)

#Draw plate
plate_points = bf.plate_points(72.91,6,[0,-6,0],[0,0,117])
#Draw servo
servo_links = [16.46,117.22]

theta1,theta2= bf.get_servo_angle(plate_points,servo_links,base_points)

#print("\n{}Finalizo correctamente{}".format("-"*35,"-"*35))
#for i in range(6):
#    print("Punto {}:\n    theta1 = {}\n    theta2 = {}".format(i,theta1[i],theta2[i]))
    

#####Graficar
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
bf.draw_axis(110,110,220,ax,fig)

bf.draw_by_points(base_points,ax,fig,'orangered')
bf.draw_by_points(plate_points,ax,fig,'dodgerblue')

bf.draw_servo(base_points,plate_points,servo_links[0],theta1,ax,fig)

servo_values = []
for i in theta1:
    servo_values.append(i[0])
print(servo_values)
#input("Enter para salir B)\n")

