#algoritmos para obtener posicion x , y del objeto en plataforma
#algoritmo para detectar si el objeto esta sobre la plataforma

import cv2
import numpy as np

def init():
    global rangomax
    global rangomin
    global cam
    cam = cv2.VideoCapture(0)
    rangomax=np.array([80,255,255])  #naranja obscuro 30
    rangomin=np.array([60,100,20])     #naranja claro 10
    #rangomax=np.array([30,255,255])  #verde obscuro
    #rangomin=np.array([10,150,150])     #verde claro
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
def position(show):
    values=(0,0,False)
    okay,frame = cam.read()
    if okay:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara=cv2.inRange(hsv,rangomin,rangomax)
        _,contornos,_=cv2.findContours(mascara,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contornos:
            area=cv2.contourArea(c)
            if area > 100:
                M=cv2.moments(c)
                if(M["m00"]==0):
                    M["m00"]=1
                x=int(M["m10"]/M["m00"])
                y=int(M["m01"]/M["m00"])
                cv2.circle(frame,(x,y),7,(0,255,0),-1)
                values=(x-320,y-220,True)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'{},{}'.format(x-320,y-220),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
                cv2.drawContours(frame,[cv2.convexHull(c)], 0,(0,255,0),3)     
        if(show==True): 
            cv2.imshow('camara', frame)
        
        k=cv2.waitKey(1) & 0xFF
    return values

#init()

#while True:
#    values=position(True)
#    x_position=values[0]
#    y_position=values[1]
#    ball_on_plate=values[2]
#    print("X={}, Y={}, Ball={}".format(x_position,y_position,ball_on_plate))
