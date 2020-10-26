from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import time
import os.path
from PIL import Image

serial = i2c(port=1,address=0x3C)
device=sh1106(serial,rotate=0)


img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
'images', 'pi_logo.png'))
logo = Image.open(img_path).convert("RGBA")
fff = Image.new(logo.mode, logo.size, (255,) * 4)
background = Image.new("RGBA", device.size, "white")
posn = ((device.width - logo.width) // 2, 0)

while True:
    for angle in range(0,1,2):
        rot = logo.rotate(angle, resample=Image.BILINEAR)
        img = Image.composite(rot, fff, rot)
        background.paste(img, posn)
        device.display(background.convert(device.mode))
 
 

