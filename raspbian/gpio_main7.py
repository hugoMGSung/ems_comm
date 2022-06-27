# Servo Motor test
import RPi.GPIO as GPIO
import time

SERVO = 12

GPIO.setmode(GPIO.BOARD) # 
GPIO.setup(SERVO, GPIO.OUT)

pwm = GPIO.PWM(SERVO, 50) # 50Hz servo motor 동작주파수
pwm.start(3.0) # 0.6ms

for cnt in range(0, 3):
    pwm.ChangeDutyCycle(3.0) # 0 
    time.sleep(0.5)
    pwm.ChangeDutyCycle(7.5) # 90
    time.sleep(0.5)
    pwm.ChangeDutyCycle(12.5) # 180
    time.sleep(0.5)

pwm.ChangeDutyCycle(0.0)
pwm.stop()
GPIO.cleanup()