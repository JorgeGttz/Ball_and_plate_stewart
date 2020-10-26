  #how the IP direction through lcd
import re,os
import RPi_I2C_driver
from time import sleep


def get_ip():
    init_comunication()
    direction= os.popen("hostname -I").read().split(' ')
    direction=direction[0]
    ipv4_pattern=re.compile("^(\d{1,3}\.){3}\d{1,3}$")
    
    if ipv4_pattern.match(direction):
         print("Match")
         ip=direction
         print(ip)
    else:
         print("No Match")
         ip=None
    return ip

def init_comunication():
    mylcd.lcd_clear()
    for i in range(1,4):
        mylcd.lcd_display_string_pos("Searching IP",1,0)
        mylcd.lcd_display_string_pos(".",1,11+i)
        sleep(0.5)
        mylcd.lcd_clear()

mylcd = RPi_I2C_driver.lcd()
ip=get_ip()

while ip == None:
    ip=get_ip()
    #print("IP not found")
    if ip is None:
        mylcd.lcd_display_string(" IP: No Found",1)
        sleep(2)

#print("IP:{}".format(ip))
mylcd.lcd_display_string(" IP: Found",1)
mylcd.lcd_display_string("IP:{}".format(ip),2)
sleep(1)
   
