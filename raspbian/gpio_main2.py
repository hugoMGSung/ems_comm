# BUTTON PUSH
import RPi.GPIO as GPIO
import time

BUTTON = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN) 

while True:
    GPIO.wait_for_edge(BUTTON, GPIO.RISING, bouncetime=100)
    time.sleep(0.1)

    print(GPIO.input(BUTTON))