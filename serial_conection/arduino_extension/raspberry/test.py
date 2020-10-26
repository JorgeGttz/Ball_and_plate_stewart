import numpy as np
from time import sleep
from threading import Timer
import serial,re,sys,cv2

#if __name__ == '__main__':
#    if len(sys.argv) == 2:
#        port = sys.argv[1]
#    else:
#        if len(sys.argv) == 0:
#            print("You should enter serial port")
#        else:
#            print("Only one parameter is allowed")
#        exit(1)

#try:
#    UPDATE_TIME = .025
#    arduino = serial.Serial('/dev/ttyACM0',115200)
#    state = "waiting"
#except:
#    print("The entered serial port is not correctly or available")
#    exit(1)

#def serial_irq():   #This function is request each .25 seconds
#    if state != "break":
#        if state == "filter_off":#Request screen information Without filter
#            arduino.write("w1,0\n")
#        if state == "filter_on":#Request screen information Without filter
#            arduino.write("f1,0\n")
#        t = Timer(UPDATE_TIME, serial_irq)
#        t.start()

#def update_screen(pos_):
#    wall_paper = cv2.imread('itcg_image.jpg')

    #cv2.putText(wall_paper,"Posicion",(90,130),cv2.FONT_ITALIC,1,(255,0,0),1)
    #cv2.putText(wall_paper,"x={:4} y={:4}".format(pos_[0],pos_[1]),(50,170),cv2.FONT_ITALIC,.65,(255,0,0),1)

#    cv2.imshow('Ball and Plate ITCG',wall_paper)
    
#t = Timer(UPDATE_TIME, serial_irq)
#t.start()
wall_paper = cv2.imread('itcg_image.jpg',1)
cv2.imshow("name",wall_paper)
cv2.waitKey(0)
cv2.destroyAllWindows()
#update_screen(['----','----'])

