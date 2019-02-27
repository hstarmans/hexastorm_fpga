import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
# reset high
print("Pin high for 3 seconds")
GPIO.output(22,1)
sleep(3)
# reset low
print("Pin low for 3 seconds")
GPIO.output(22,0)
sleep(3)

