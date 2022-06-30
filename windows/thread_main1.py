# 스레드없이 동작
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget): # QMainWindow로 변경요
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/threadtask.ui', self) # UI파일 변경요        
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.show()

    def btnStartClicked(self):
        self.pgbTask.setRange(0, 999999)
        for i in range(0, 1000000):
            print(f'출력 > {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'출력 > {i}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()