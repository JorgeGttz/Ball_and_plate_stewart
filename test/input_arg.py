#This is an example about how to enter data in serial
import sys,re

if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = sys.argv[1]
        patron = re.compile(r'[/dev/ttyS]')

        if patron.match(port):
            print("Correcto")
        else:
            print("Incorrecto")
    else:
        if len(sys.argv) == 0:
            print("You should enter serial port")
        else:
            print("Only one parameter is allowed")
        exit(1)

print("Serial port is at {}".format(port))
