## 동시에 두가지태스크
from threading import Thread, Timer
import time
import paho.mqtt.client as mqtt
import json
import datetime as dt

class publisher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = '127.0.0.1'
        self.port = 1883
        print('publisher 스레드 시작')
        self.client = mqtt.Client(client_id='EMS101')

    def run(self):
        self.client.connect(self.host, self.port)
        self.publish_data_auto()        

    def publish_data_auto(self):
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'DASHBOARD', 'CURR_DT' : curr,
                       'TYPE': 'DEHUMD', 'STAT' : 'ON' }  # AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                            payload=pub_data)
        print('Published')
        Timer(3.0, self.publish_data_auto).start()

class subscriber(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = '127.0.0.1' # 추후 변경
        self.port = 1883        
        print('subscriber 스레드 시작')
        self.client = mqtt.Client(client_id='EMS001')

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'sub:connected with rc > {rc}')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        print(f'{msg.topic} / {rcv_msg}')
        time.sleep(2.0)

    def run(self):
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/data/')
        self.client.loop_forever()

if __name__ == '__main__':
    thPub = publisher()
    thSub = subscriber()
    thPub.start()    
    thSub.start()