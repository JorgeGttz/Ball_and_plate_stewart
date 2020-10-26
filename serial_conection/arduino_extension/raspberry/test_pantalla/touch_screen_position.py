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

try:
    UPDATE_TIME = .025
    arduino = serial.Serial("/dev/ttyACM0",115200)
    state = "waiting"
except:
    print("The entered serial port is not correctly or available")
    exit(1)



def update_screen(pos_):
    wall_paper = cv2.imread('itcg_image.jpg')

    cv2.putText(wall_paper,"Posicion",(90,130),cv2.FONT_ITALIC,1,(255,0,0),1)
    cv2.putText(wall_paper,"x={:4} y={:4}".format(pos_[0],pos_[1]),(50,170),cv2.FONT_ITALIC,.65,(255,0,0),1)

    cv2.imshow('Ball and Plate ITCG',wall_paper)

def serial_irq():   #This function is request each .25 seconds
    if state != "break":
        if state == "filter_off":#Request screen information Without filter
            arduino.write(str.encode("w1,0\n"))
        elif state == "filter_on":#Request screen information Without filter
            arduino.write(str.encode("f1,0\n"))
        t = Timer(UPDATE_TIME, serial_irq)
        t.start()
        
t = Timer(UPDATE_TIME, serial_irq)
t.start()

update_screen(['----','----'])

while state != "break":
    try:
        if arduino.inWaiting() > 0:
            ##Read the serial port
            serial_input = arduino.readline()
            message = serial_input
            serial_input = serial_input[:-2].decode('utf-8') #Remove \n of expression

            matcher = re.compile(r'[A-Za-z][-]?[0-9]+([,][-]?[0-9]+)*$')
            #Verify the input
            if matcher.match(serial_input):
                char = serial_input[0]
                digits = serial_input[1:]

                if digits.find(','):
                    digits = digits.split(',')

                if len(digits) == 2 and char == 'p':   ##If enter 2 numbers
                    pos=[digits[0],digits[1]]
                    #Updating position values
                    if pos[0] == '1500':
                        wall_paper = cv2.imread('itcg_image.jpg')
                        cv2.putText(wall_paper,"Posicion",(90,130),cv2.FONT_ITALIC,1,(255,0,0),1)
                        cv2.putText(wall_paper,"NULL",(125,170),cv2.FONT_ITALIC,.6,(255,0,0),1)

                        cv2.imshow('Ball and Plate ITCG',wall_paper)
                    else:
                        update_screen(pos)
            else:
                print("Expression doesn't match")
                print(message)
                update_screen(['xxxx','xxxx'])
        if state == "waiting":
            update_screen(['----','----'])   
        key = cv2.waitKey(1) & 0xFF

        if key == ord('w'):
            state = "filter_off"
        elif key == ord('f'):
            state = "filter_on"
        elif key == ord('s'):
            update_screen(['----','----'])
            state = "waiting"
            arduino.write(str.encode("s0,0\n"))
        elif key == ord('b'):
            print("Closing... application")
            state = "break"
            arduino.close()
            cv2.destroyAllWindows()
            break;


    except KeyboardInterrupt:
        print("Closing... application")
        state = "break"
        arduino.close()
        cv2.destroyAllWindows()
        break

