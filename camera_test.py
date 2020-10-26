from picamera import PiCamera
from time import sleep
#Se modifico

camera = PiCamera()

print("Initializing")
camera.start_preview()
sleep(10)
print("chido one")
camera.stop_preview()
