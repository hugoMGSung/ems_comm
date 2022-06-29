# EMS 대시보드앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import requests
import json 
import dashboard_rc # 리소스 py파일 추가

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()

    def initUI(self):
        uic.loadUi('./windows/ui/dashboard.ui', self)
        self.setWindowIcon(QIcon('iot_64.png'))

        self.show()

    def showWeather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather' \
              '?q=seoul&appid=0a9f6aeb854114111d15d53b5a76469d' \
              '&lang=kr&units=metric'
        result = requests.get(url)
        result = json.loads(result.text)
        weather = result['weather'][0]['main'].lower()
        print(weather)
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