from gpiozero import Button, LED
from signal import pause
from time import sleep
from picamera import PiCamera
from datetime import datetime
from random import randint


button = Button(14, pull_up = False)
led = LED(15)

camera = PiCamera()
camera.iso = 100

camera.start_preview()
sleep(2)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g


def send_signal():
    global led
    global camera
    print("Pressed")
    led.on()
    sleep(1)
    timeStr = str(datetime.now().isoformat) + str(randint(0, 10))
    print("Image name: " + timeStr)
    camera.capture(timeStr, 'jpeg')


print("Started...")
button.when_pressed = send_signal

pause()