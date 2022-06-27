import Adafruit_DHT as dht
import time

sensor = dht.DHT11
PIN = 4  # GPIO.BCM mode

try:
    while True:
        (humid, temp) = dht.read_retry(sensor, PIN)
        if humid is not None and temp is not None:
            print(f'Temp > {temp:.1f} C / Humidity > {humid:.1f}')
        else:
            print('Sensor error!')
        
        time.sleep(1.0) # 1 second delay
except KeyboardInterrupt:
    print('End of program')