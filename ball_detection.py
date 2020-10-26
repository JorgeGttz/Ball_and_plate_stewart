import cv2
import numpy as np
 
cam=cv2.VideoCapture(0)
kernel=np.ones((5,5),np.uint8)
 
while(True):
    ret,frame=cam.read()
    rangomax=np.array([50,255,50])  #verde claro
    rangomin=np.array([0,40,0])     #verde obscuro
    mascara=cv2.inRange(frame,rangomin,rangomax)
    #opening=cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    _,contornos,_=cv2.findContours(mascara,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    
    for c in contornos:
        area=cv2.contourArea(c)
        if area > 1000:
            M=cv2.moments(c)
            if(M["m00"]==0): M["m00"]=1
            x=int(M["m10"]/M["m00"])
            y=int(M["m01"]/M["m00"])
            cv2.circle(frame,(x,y),7,(0,255,0),-1)
            font=cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'{},{}'.format(x-320,y-220),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
            cv2.drawContours(frame,[cv2.convexHull(c)], 0,(0,255,0),3)

    cv2.imshow('camara',frame)
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break
                                                                                                                                                                                             
                              
