from gpiozero import LED
from signal import pause

red = LED(14)

red.blink()

pause()