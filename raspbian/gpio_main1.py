# RGB LED ON/OFF
import RPi.GPIO as GPIO
import time

RED = 11
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD) # GPIO.BCM
GPIO.setup(RED, GPIO.OUT) # 11핀 출력셋팅
GPIO.setup(GREEN, GPIO.OUT) # 12핀 출력셋팅
GPIO.setup(BLUE, GPIO.OUT) # 13핀 출력셋팅

try:
    while True:
        GPIO.output(RED, GPIO.HIGH) # on
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH) # on
        GPIO.output(BLUE, GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH) # on
        time.sleep(0.5)

        GPIO.output(RED, GPIO.HIGH) # on
        GPIO.output(GREEN, GPIO.HIGH) # on
        GPIO.output(BLUE, GPIO.HIGH) # on
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)
    GPIO.cleanup()