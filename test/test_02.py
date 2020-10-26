import numpy as np
import cv2
from time import sleep
import serial,re

UPDATE_TIME = .25

arduino = serial.Serial('COM1',115200)
pos=[2,3]
state = "waiting"


while state != "break":
    try:
        char = arduino.readline()
        print(char)
        
        wall_paper = cv2.imread('itcg_image.jpg')
        cv2.putText(wall_paper,"Posicion",(90,130),cv2.FONT_ITALIC,1,(255,0,0),1,cv2.LINE_AA)
        cv2.putText(wall_paper,"x={:3} y={:3}".format(pos[0],pos[1]),(50,170),cv2.FONT_ITALIC,.9,(255,0,0),1,cv2.LINE_AA)
        #cv2.putText(wall_paper,"Posicion",(50,120),cv2.FONT_ITALIC,1,(255,0,0),1,cv2.LINE_AA)
        cv2.imshow('Ball and Plate ITCG',wall_paper)

        key = cv2.waitKey(1) & 0xFF
        if  key == ord('b'):
            state = "break"
            break
        elif key == ord('w'):
            state = "filter_off"
        elif key == ord('f'):
            state = "filter_on"
        elif key == ord('s'):
            state = "waiting"
            sleep(0.1)
    except KeyboardInterrupt:
            print("Exiting")
            break
arduino.close()
cv2.destroyAllWindows()
