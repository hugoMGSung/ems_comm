# PAN test
import RPi.GPIO as GPIO
import time

PAN = 13

GPIO.setmode(GPIO.BOARD) # 
GPIO.setup(PAN, GPIO.OUT)

try:
    while True:
        GPIO.output(PAN, GPIO.HIGH)
        time.sleep(5.0)

        GPIO.output(PAN, GPIO.LOW)
        time.sleep(5.0)

except KeyboardInterrupt:
    GPIO.cleanup()

