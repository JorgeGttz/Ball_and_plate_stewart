import serial

arduino = serial.Serial('/dev/ttyACM0',115200)

while True:
    command = raw_input('Enter code: ')
    arduino.write(command)

    if command == '0':
        print("Led OFF")
    elif command == '1':
        print("Led On")
    elif command == 'b':
        print("Clossing app .. ")
        break

arduino.write('0')
arduino.close()
