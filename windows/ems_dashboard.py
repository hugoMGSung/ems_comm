# EMS 대시보드앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import requests
import json 
import dashboard_rc # 리소스 py파일 추가
import time
import datetime as dt
import paho.mqtt.client as mqtt # mqtt subscribe를 위해서 추가

# pip install PyMySQL
import pymysql

# pip install pyqtgraph
# pip install pyqtchart
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from PyQt5.QtChart import *
from collections import deque

broker_url = 'localhost' # 로컬에 MQTT broker가 같이 설치되어 있으므로 

class Worker(QThread):
    sigStatus = pyqtSignal(str) # 연결상태 시그널, 부모클래스 MyApp 전달용
    sigMessage = pyqtSignal(dict) # MQTT Subscribe 시그널, MyApp 전달 딕셔너리형

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.host = broker_url
        self.port = 1883
        self.client = mqtt.Client(client_id='Dashboard')

    def onConnect(self, mqttc, obj, flags, rc):
        try:
            print(f'connected with result code > {rc}')
            self.sigStatus.emit('SUCCEED') # MyApp으로 성공메시지 전달
        except Exception as e:
            print(f'error > {e.args}')
            self.sigStatus.emit('FAILED')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        # print(f'{msg.topic} / {rcv_msg}') # 시그널로 전달했으므로 주석처리
        self.sigMessage.emit(json.loads(rcv_msg))
        time.sleep(2.0)

    def mqttloop(self):
        self.client.loop()
        print('MQTT client loop')

    def run(self): # Thread에서는 run() 필수
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/data/')
        self.client.loop_forever()

class MyApp(QMainWindow):
    isTempAlarmed = False  # 알람여부
    isHumidAlarmed = False
    tempData = humidData = None
    idx = 0
    isTempShow = True

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()
        self.initThread()
        self.initChart()

    # 엄청 복잡합니다. 각오가 필요합니다 ^^
    def initChart(self):
        self.btnTemp.clicked.connect(self.btnTempShowClicked)
        self.btnHumid.clicked.connect(self.btnHumidShowClicked)

        self.traces = dict()
        self.timestamp = 0
        self.timeaxis = [] # 시간축(x)
        self.tempaxis = [] # 온도리스트
        self.humidaxis = [] # 습도
        self.graph_lim = 15 # 그래프 초기화
        self.deque_timestamp = deque([], maxlen=self.graph_lim+20)
        self.deque_temp = deque([], maxlen=self.graph_lim+20)
        self.deque_humid = deque([], maxlen=self.graph_lim+20)

        self.graphwidget1 = PlotWidget(title="Temperature")
        x1_axis = self.graphwidget1.getAxis('bottom')
        x1_axis.setLabel(text=' ')
        y1_axis = self.graphwidget1.getAxis('left')
        y1_axis.setLabel(text='Temp')

        self.graphwidget2 = PlotWidget(title="Humidity")
        x2_axis = self.graphwidget2.getAxis('bottom')
        x2_axis.setLabel(text=' ')
        y2_axis = self.graphwidget2.getAxis('left')
        y2_axis.setLabel(text='Humid')

        self.dataView.addWidget(self.graphwidget1, 0, 0, 0, 3)
        self.dataView.addWidget(self.graphwidget2, 0, 0, 0, 3)
        self.graphwidget1.show()
        self.graphwidget2.hide()

    def btnTempShowClicked(self):
        self.graphwidget1.show()
        self.graphwidget2.hide()
        isTempShow = True

    def btnHumidShowClicked(self):
        self.graphwidget1.hide()
        self.graphwidget2.show()
        isTempShow = False
        
    def initThread(self):
        self.myThread = Worker(self)
        self.myThread.sigStatus.connect(self.updateStatus)
        self.myThread.sigMessage.connect(self.updateMessage)
        self.myThread.start()

    @pyqtSlot(dict)
    def updateMessage(self, data):
        # 1. json변환
        # 2. Label에 Device명칭 업데이트
        # 3. 온도라벨, 습도라벨 현재 온도,습도 업데이트
        # 4. MySQL DB에 입력
        # 5. 이상기온 알람
        # 6. txbLog 로그 출력 / 다시 제거
        # 7. Chart 데이터 추가
        print(data)
        dev_id = data['DEV_ID'] # 2.        
        self.lblTempTitle.setText(f'{dev_id} Temperature')
        self.lblHumidTitle.setText(f'{dev_id} Humidity')
        temp = data['TEMP'] # 3.
        humid = data['HUMID']
        self.lblCurrTemp.setText(f'{temp:.1f}')
        self.lblCurrHumid.setText(f'{humid:.0f}')
        # self.txbLog.append(json.dumps(data))
        # self.dialHumid.setValue(int(humid)) 220701 위젯 삭제
        # 5.
        if temp >= 30.0:            
            self.lblTempAlarm.setText(f'{dev_id} 이상기온감지')
            #self.btnTempAlarm.setEnabled(True) # 버튼활성화
            #self.btnTempStop.setEnabled(False)
            if self.isTempAlarmed == False:
                self.isTempAlarmed = True
                QMessageBox.warning(self, '경고', f'{dev_id}에서 이상기온감지!!!')

        elif temp <= 26.5:
            self.lblTempAlarm.setText(f'{dev_id} 정상기온')
            self.isTempAlarmed = False
            #self.btnTempAlarm.setEnabled(False) # 버튼비활성화
            #self.btnTempStop.setEnabled(True)

        if humid >= 85.0:
            self.lblHumidAlarm.setText(f'{dev_id} 이상습도감지')
            if self.isHumidAlarmed == False:
                self.isHumidAlarmed = True
                QMessageBox.warning(self, '경고', f'{dev_id}에서 이상습도감지!!!')
        elif humid <= 65.0:
            self.lblHumidAlarm.setText(f'{dev_id} 정상습도')
            self.isHumidAlarmed = False

        # 4. DB입력
        # self.conn = pymysql.connect(host='127.0.0.1',
        #                             user='root',
        #                             password='1234',
        #                             db='bms',
        #                             charset='euckr')

        curr_dt = data['CURR_DT']
        # query = '''INSERT INTO ems_data
        #                 (dev_id, curr_dt, temp, humid)
        #             VALUES 
        #                 (%s, %s, %s, %s) '''
        
        # with self.conn:
        #     with self.conn.cursor() as cur:
        #         cur.execute(query, (dev_id, curr_dt, temp, humid))
        #         self.conn.commit()
        #         print('DB Inserted!')
        # chart 업데이트
        self.updateChart(curr_dt, temp, humid)

    def updateChart(self, curr_dt, temp, humid):
        self.timestamp += 1

        self.deque_timestamp.append(self.timestamp)
        self.deque_temp.append(temp)
        self.deque_humid.append(humid)

        timeaxis_list = list(self.deque_timestamp)

        if self.isTempShow == True:
            temp_list = list(self.deque_temp)

            if self.timestamp > self.graph_lim:
                self.graphwidget1.setRange(xRange=[self.timestamp-self.graph_lim+1, self.timestamp], yRange=[
                                        min(temp_list[-self.graph_lim:]), max(temp_list[-self.graph_lim:])])
            self.set_plotdata(name="temp", data_x=timeaxis_list,
                            data_y=temp_list)
        else:
            humid_list = list(self.deque_humid)

            if self.timestamp > self.graph_lim:
                self.graphwidget2.setRange(xRange=[self.timestamp-self.graph_lim+1, self.timestamp], yRange=[
                                        min(humid_list[-self.graph_lim:]), max(humid_list[-self.graph_lim:])])
            self.set_plotdata(name="humid", data_x=timeaxis_list,
                            data_y=humid_list)
        print('Chart updated!!')

    def set_plotdata(self, name, data_x, data_y):
        # print('set_data')
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == "temp":
                self.traces[name] = self.graphwidget1.getPlotItem().plot(
                    pen=pg.mkPen((85, 170, 255), width=3))

    @pyqtSlot(str)
    def updateStatus(self, stat):
        # background-image: url(:/red);
        # background-repeat: none;
        # border: none;
        if stat == 'SUCCEED':
            self.lblStatus.setText('Connected!')
            self.connFrame.setStyleSheet(
                'background-image: url(:/green);'
                'background-repeat: none;'
                'border: none;'
            )
        else:
            self.lblStatus.setText('Disconnected~')
            self.connFrame.setStyleSheet(
                'background-image: url(:/red);'
                'background-repeat: none;'
                'border: none;'
            )

    def initUI(self):        
        uic.loadUi('./windows/ui/dashboard.ui', self)
        self.setWindowIcon(QIcon('iot_24.png'))
        # 화면 정중앙 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())  # End of screen central position
        #self.btnTempAlarm.setEnabled(False) # 버튼비활성화
        #self.btnTempStop.setEnabled(True)
        # 위젯 시그널 정의
        self.btnTempAlarm.clicked.connect(self.btnTempAlarmClicked)
        self.btnTempStop.clicked.connect(self.btnTempStopClicked)
        self.btnHumidAlarm.clicked.connect(self.btnHumidAlarmClicked)
        self.btnHumidStop.clicked.connect(self.btnHumidStopClicked)
        self.show()

    def btnHumidAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상습도로 제습기 가동')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT' : curr,
                       'TYPE': 'DEHUMD', 'STAT' : 'ON' }  # DEHUMD
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                            payload=pub_data)
        print('Dehumidufier On Published')
        self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'ON')
    
    def btnHumidStopClicked(self):
        QMessageBox.information(self, '정상', '제습기 중지')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT' : curr,
                       'TYPE': 'DEHUMD', 'STAT' : 'OFF' }
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                            payload=pub_data)
        print('Dehumidufier Off Published')
        self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'OFF')

    def btnTempAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상온도로 에어컨 가동')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT' : curr,
                       'TYPE': 'AIRCON', 'STAT' : 'ON' }  # AIRCON
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                            payload=pub_data)
        print('AIRCON On Published')
        self.insertAlarmData('CONTROL', curr, 'AIRCON', 'ON')

    def btnTempStopClicked(self):
        QMessageBox.information(self, '정상', '에어컨 중지')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':'CONTROL', 'CURR_DT' : curr,
                       'TYPE': 'AIRCON', 'STAT' : 'OFF' }
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/',
                            payload=pub_data)
        print('AIRCON Off Published')
        self.insertAlarmData('CONTROL', curr, 'AIRCON', 'OFF')

    # 이상상태,정상상태 DB저장함수
    def insertAlarmData(self, dev_id, curr_dt, types, stat):
        pass
        # self.conn = pymysql.connect(host='127.0.0.1',
        #                             user='root',
        #                             password='1234',
        #                             db='bms',
        #                             charset='euckr')

        # query = '''INSERT INTO ems_alarm
        #                 (dev_id, curr_dt, type, stat)
        #             VALUES 
        #                 (%s, %s, %s, %s) '''
        
        # with self.conn:
        #     with self.conn.cursor() as cur:
        #         cur.execute(query, (dev_id, curr_dt, types, stat))
        #         self.conn.commit()
        #         print('Alarm Inserted!')

    
    # 종료 메시지박스
    def closeEvent(self, signal):
        ans = QMessageBox.question(self, '종료', '종료하시겠습니까?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if ans == QMessageBox.Yes:
            signal.accept()
        else:
            signal.ignore()

    def showWeather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather' \
              '?q=seoul&appid=0a9f6aeb854114111d15d53b5a76469d' \
              '&lang=kr&units=metric'
        result = requests.get(url)
        result = json.loads(result.text)
        print(result)
        weather = result['weather'][0]['main'].lower()
        # print(weather)
        self.weatherFrame.setStyleSheet(
            (
                f'background-image: url(:/{weather});'
                'background-repeat: none;'
                'border: none;'
            )
        )
    
    def showTime(self):
        today = QDateTime.currentDateTime()
        currDate = today.date()
        currTime = today.time()
        currDay = today.toString('dddd')

        self.lblDate.setText(currDate.toString('yyyy-MM-dd'))
        self.lblDay.setText(currDay)
        self.lblTime.setText(currTime.toString('HH:mm'))
        if today.time().hour() > 5 and today.time().hour() < 12:
            self.lblGreeting.setText('Good Morning!')
        elif today.time().hour() >= 12 and today.time().hour() < 18:
            self.lblGreeting.setText('Good Afternoon!')
        elif today.time().hour() >= 18:
            self.lblGreeting.setText('Good Evening!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()