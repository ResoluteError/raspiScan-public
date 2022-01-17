from time import sleep, time
from picamera import PiCamera
from datetime import datetime
from random import randint

camera = PiCamera()
camera.iso = 400

camera.start_preview()
sleep(2)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
sleep(1)


def take_pic():
    global camera
    print("Taking Pic")
    imageName = str(datetime.now().isoformat()) + str(randint(0, 10))
    print("Image name: " + imageName)
    preImage = round(time() * 1000)
    camera.capture(imageName, 'jpeg')
    postImage = round(time() * 1000)
    print("Pic taken - time: " + str(postImage - preImage))


print("Started...")
take_pic()
