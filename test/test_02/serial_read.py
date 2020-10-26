import serial

arduino = serial.Serial('/dev/ttyACM0',115200)

def serial_actions(com_port):
    try:
        new_char = com_port.readline()
        new_char = new_char[:-1]
        print("Se recibio {}".format(new_char))
    except:
        pass

while True:
    serial_actions(arduino)

