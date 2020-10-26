import cv2
import numpy as np

cap = cv2.VideoCapture(0)
kernel = np.ones((5,5),np.uint8)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #Estos valores los modifique a lo pendejo segun mi iluminacion, el 10 el 30 y los dos 255 no los muevas, vas a tener que jugar con los otros dos
    #originalmente para detectar naranja es  100 y 29 donde estan los 150, esos tendria que modificar si ves que no esta detectando bien, yo puse doble 150 por que con el rojo detectaba chingon ajajaj realmente no tengo una razon de por que esos valores
    
    lower_orang = np.array([10,150,150]) 
    upper_orang = np.array([30,255,255])

    mask = cv2.inRange(hsv, lower_orang, upper_orang)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernel)
    
    
    x,y,w,h = cv2.boundingRect(opening)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
   
    cv2.circle(frame,(int(x+w/2),int(y+h/2)),5,(255,0,0),-1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    t=str(x)
    cv2.putText(frame,t,(50,470), font, 0.8, (200,255,155), 2, cv2.LINE_AA)
    cv2.putText(frame,'X=',(10,470), font, 0.8, (0,0,255), 2, cv2.LINE_AA)
    p=str(y)
    cv2.putText(frame,p,(150,470), font, 0.8, (200,255,155), 2, cv2.LINE_AA)
    cv2.putText(frame,'Y=',(110,470), font, 0.8, (0,0,255), 2, cv2.LINE_AA)


    cv2.imshow('Camara',frame)

    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
        
cv2.destroyAllWindows
cap.release()
