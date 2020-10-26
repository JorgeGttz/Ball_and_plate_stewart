#pruebas para la libreria
import time_interruption
import time

integartion_time.time_interruption.ticker()
integartion_time.time_interruption.init()  

while True:
    time.sleep()
    print("ticker={}".format(integartion_time.time_interruption.ticker()))
    if(integartion_time.time_interruption.ticker() > 10):
        integartion_time.time_interruption.ticker() = 0
