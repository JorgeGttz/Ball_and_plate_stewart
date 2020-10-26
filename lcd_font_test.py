from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time
from PIL import ImageFont, ImageDraw


serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=0)

# Box and text rendered in portrait mode
with canvas(device) as draw:
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf",16)
    draw.text((0,0), "Hello World, here I am", font=font, fill=255)
    draw.text((0,15),"Hello", font=font, fill=255)
    draw.text((0,30),"Hello", font=font, fill=255)
    draw.text((0,45),"Hello", font=font, fill=255)
#raw_input("Enter to Exit")

while 1:
    time.sleep(1)
