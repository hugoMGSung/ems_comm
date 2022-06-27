# Servo Motor test
import RPi.GPIO as GPIO
import time

SERVO = 12

GPIO.setmode(GPIO.BOARD) # 
GPIO.setup(SERVO, GPIO.OUT)

pwm = GPIO.PWM(SERVO, 50) # 50Hz
pwm.start(3.0) # 0.6ms

time.sleep(2.0) # 2sec
pwm.ChangeDutyCycle(0.0)

pwm.stop()
GPIO.cleanup()