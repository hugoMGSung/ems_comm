import adafruit_dht as dht
import board
import time

device = dht.DHT22(board.D4)

while True:
    try:
        temp = device.temperature
        humid = device.humidity
        print(f'Temp > {temp:.1f} C / Humidity > {humid:.1f}')

    except RuntimeError as e:
        print(e.args[0])
        time.sleep(1.0)

    except Exception as e:
        device.exit()
        raise e

    time.sleep(1.0)

