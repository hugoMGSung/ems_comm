# MQTT Publisher
# sudo pip install paho-mqtt
import threading
import datetime as dt
import paho.mqtt.client as mqtt
import json

client2 = None
count = 0

def publish_sensor_data():
    curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    origin_data = { 'DEV_ID' : 'EMS01', 'CURR_DT' : curr,
                    'TEMP' : 25.4, 'HUMID' : 60 }
    pub_data = json.dumps(origin_data)
    client2.publish(topic='ems/rasp/data/',
                    payload=pub_data)
    print(f'{curr} -> MQTT Published')
    
    threading.Timer(2.0, publish_sensor_data).start()

if __name__ == '__main__':
    broker_url = '192.168.0.17'
    client2 = mqtt.Client(client_id='EMS01')
    client2.connect(host=broker_url,
                    port=1883)

    publish_sensor_data()