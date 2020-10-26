#algoritmos para obtener posicion x , y del objeto en plataforma
#algoritmo para detectar si el objeto esta sobre la plataforma

import cv2
import numpy as np

#verde obscuro [80,255,255]
#verde claro   [60,100,20]
#naranja obscuro [30,255,255]
#naranja clar  [10,150,150]

class color_range:
    def __init__(self,name,rangomax,rangomin):
        self.name=name
        self.rangomax=np.array(rangomax)  #naranja obscuro 30
        self.rangomin=np.array(rangomin)     #naranja claro 10
    
    def __str__(self):
        return "Color= %s Rangomax = %s, Rangomin = %s"                                     %(self.name,self.rangomax,self.rangomin)    
    
    def __repr__(self):
        return str(self)

class COLORS:
    NARANJA=color_range("naranja",[30,255,255],[10,150,150])
    VERDE  =color_range("verde",[80,255,255],[60,100,20])
    
map_string_to_color={
    "naranja": COLORS.NARANJA,
    "verde" :  COLORS.VERDE
}
 
class ball_position:
    def __init__(self,x,y,ball_on_plate):
        self.default_x=x
        self.default_y=y
        self.default_ball_on_plate=ball_on_plate
        self.set_default_values()           

    def set_default_values(self):   
        self.x=self.default_x
        self.y=self.default_y
        self.ball_on_plate=self.default_ball_on_plate

    def set_values(self,x,y,ball_on_plate):
        self.x=x
        self.y=y
        self.ball_on_plate=ball_on_plate
        
    def __str__(self):
        return "X= %d, Y= %d, Ball_on=%s" %(self.x,self.y,self.ball_on_plate)
    
    def __repr__(self):
        return str(self)


class ball_info:   

    def __init__(self,color):
        self.color=self.__get_color_object__(color)        
        self.cam = cv2.VideoCapture(1)
        self.position=ball_position(0,0,False)

    def __get_color_object__(self,color):
        if isinstance (color,color_range):
            return color
        elif isinstance (color,str):
            if color in map_string_to_color.keys():
                return map_string_to_color[color]
            else:
                raise Exception("Color entered {} is not on list, try it with other color. Available colors {}" .format(color,map_string_to_color.keys()) )
        else:   
            raise Exception("Entered color{}, is not instance of color range".format(color))
                
    def update_position(self,show=False):
        ret,frame = self.cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara=cv2.inRange(hsv,self.color.rangomin,self.color.rangomax)
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
                self.position.set_values(x-320,y-220,True)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'{},{}'.format(x-320,y-220),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
                cv2.drawContours(frame,[cv2.convexHull(c)], 0,(0,255,0),3)

            else:
                self.position.set_default_values()  
        if show:    
            cv2.imshow('camara', frame)
        k=cv2.waitKey(1) & 0xFF    
  
def main():
    rc=0
    ball=ball_info("verde")
    try:
        while True:
            ball.update_position(True)
            print(ball.position)
    except KeyboardInterrupt:
        print("Closing program")
    except:
        print("unexpected error :(")
        rc=1    
    finally:
        cv2.destroyAllWindows()
    return rc

if __name__== "__main__":
    exit(main())

#while True:
#    values=position(True)
#    x_position=values[0]
#    y_position=values[1]
#    ball_on_plate=values[2]
