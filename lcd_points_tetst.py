from PIL import ImageFont, ImageDraw
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time

serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=0)

# Box and text rendered in portrait mode
with canvas(device) as draw:
    for i in range(9):
        draw.point((2+i,9),fill=255)
    for i in range(4):
        draw.point((10-i,8-i),fill=255)
        draw.point((10-i,10+i),fill=255)

#raw_input("Enter to Exit")
while 1:
    time.sleep(1)
