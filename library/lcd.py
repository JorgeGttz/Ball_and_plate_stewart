#libreria para lcd.oled.i2c con controlador sh1106

#funciones
# lcd.init()
#lcd.write(x,y,"text")
#lcd.clear()
#lcd.logo("logo")
#lcd.puntero(x) (0-3)

from luma.core.interface.serial import i2c  #libreria para comuncacion con lcd.oled 1.3"
from luma.core.render import canvas         
from luma.oled.device import sh1106
from PIL import ImageFont, ImageDraw, Image #libreria para imagenes en lcd
import os.path
import time


def init():                                 #inicializar lcd
    global device
    global font
    serial = i2c(port=1, address=0x3C)      #puerto de raspberry y address del dispositivo
    device = sh1106(serial, rotate=0)       #seleccion del driver del lcd             
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf",16)    #tipo de letra(direccion) y tamaño    

def write(text0,text1,text2,text3,puntero,line):        #write(texto0,texto1,texto2,texto3,(True/Flase),linea_puntero)
    with canvas(device) as draw:    
        #font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf",16)
        draw.text((12,0),text0,font=font, fill="white")
        draw.text((12,15),text1,font=font, fill="white")
        draw.text((12,30),text2,font=font, fill="white")
        draw.text((12,45),text3,font=font, fill="white")
        
        if puntero is True:
            for i in range(9):
                draw.point((2+i,9+(line*15)),fill="white")
            for i in range(4):
                draw.point((10-i,8-i+(line*15)),fill="white")
                draw.point((10-i,10+i+(line*15)),fill="white")
        

def clear_all():                            #limpiar pantalla completa
    with canvas(device) as draw:
        draw.text((0,0)," ",font=font, fill="white")    

def logo(logo):                             #logo de itcg,addictronics,tnm,pi_logo
    if logo is "tnm":
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'tnm.png'))
    elif logo is "addictronics":
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'addictronics.png'))
    elif logo is "itcg":
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'itcg.png'))
    elif logo is "raspi":
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'pi_logo.png'))

    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, "white")
    posn = ((device.width - logo.width) // 2, 0)
    
    rot = logo.rotate(0,resample=Image.BILINEAR)
    img=Image.composite(rot,fff,rot)
    background.paste(img, posn)
    device.display(background.convert(device.mode))

def message(text0,text1):
    with canvas(device) as draw:
        draw.text((0,15),text0,font=font, fill="white")
        draw.text((0,30),text1,font=font, fill="white")                    
