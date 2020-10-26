#libreria para modulo adc PCF8591

import smbus
import time

#Carga para modulo para i2c
miADC = smbus.SMBus(1)

# x = canal a leer (1-4)

def read(x):
    #Configuracion del registro del integrado
    miADC.write_byte_data(0x48, (0x40+x),x)
    time.sleep(0.002)
    lectura = miADC.read_byte(0x48) #read adc
    return lectura


