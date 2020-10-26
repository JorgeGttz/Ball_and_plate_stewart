import serial,re,sys
from time import sleep

arduino = serial.Serial('/dev/ttyACM0',115200)

#class serial_action:
#    def __init__(self,char,function,help_string):
#        self.char = char
#        self.callback = function
#        self.help_string =  help_string
#
#def get_screen():
#    pass
#
#serial_actions=[]
#serial_actions.append(serial_action('d',get_screen,"Get the x,y position"))


def serial_monitor(port):
    try:
        serial_input = port.readline()
        serial_input = serial_input[:-2] #Remove \n of expression

        matcher = re.compile(r'[A-Za-z][0-9]+([,][0-9]+)*$')

        if matcher.match(serial_input):
            char = serial_input[0]
            digits = serial_input[1:]

            if digits.find(','):
                digits = digits.split(',')
        else:
            print("Expression doesn't match")

        print ("Your char was {}, The numbers were: {}".format(char,digits))

        if char == 'b':
            port.close()
            return False

        return True

    except:
        return True

def test_monitor():
    while True:
        if serial_monitor(arduino) == False:
            break

while True:
    answer = raw_input("What would you like to do?\n    -1)Test serial port\n    -2)Exit\n ")
    if answer == "1":
        print("Starting Test serial port ...")
        sleep(1)
        arduino.write("s")
        test_monitor()
    elif answer == "2":
        break;
    else:
        print("No valid command")
