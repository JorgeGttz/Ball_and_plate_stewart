#algoritmos para obtener posicion x , y del objeto en plataforma
#algoritmo para detectar si el objeto esta sobre la plataforma

import cv2
import numpy as np
from time import time


video = cv2.VideoCapture(0)
rangomax=np.array([30,255,255])  #naranja obscuro
rangomin=np.array([10,150,150])     #naranja claro

def position():
    values=(0,0,False)
    tiempo_inicial=time()
    okay,image = video.read()
    if okay:     
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mascara=cv2.inRange(hsv,rangomin,rangomax)
        _,contornos,_=cv2.findContours(mascara,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
        for c in contornos:
            area=cv2.contourArea(c)
            if area > 1000:
                M=cv2.moments(c)
                if(M["m00"]==0): M["m00"]=1
                x=int(M["m10"]/M["m00"])
                y=int(M["m01"]/M["m00"])
                cv2.circle(image,(x,y),7,(0,255,0),-1)
                values=(x-320,y-220,True)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image,'{},{}'.format(x-320,y-220),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
                cv2.drawContours(image,[cv2.convexHull(c)], 0,(0,255,0),3)
                
        cv2.imshow("Images",image)
        tiempo_final=time()
        tiempo_ejecucion=tiempo_final - tiempo_inicial
        print("Time:{}".format(tiempo_ejecucion*1000)+ "ms")
        if cv2.waitKey(1) & 0xFF == ord('b'): pass
    return values

tiempo_inicial=time()

while True:
    values=position()
    x_position=values[0]
    y_position=values[1]
    ball_on_plate=values[2]
    print("X={}, Y={}".format(x_position,y_position))
    

video.release()
cv2.destroyAllWindows()
