#testa de posicion

from library import camera
from time import sleep

camera.init()

while True:

    values=camera.position()
    x_position=values[0]
    y_position=values[1]
    ball_on_plate=values[2]

    print("X:{}, Y:{}, Ball:{}".format(x_position,y_position,ball_on_plate))
    #sleep(0.01)
