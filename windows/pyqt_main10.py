## Servo Control UI
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Servo Motor Control')
        # 윈도우 기본설정
        self.setGeometry(100, 100, 300, 350)

        self.dial = QDial(self)
        self.dial.setRange(0, 13)

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 15))
        self.label.setText('Servo Motor Control')
        self.label.setAlignment(Qt.AlignCenter) # 라벨 정중앙

        # 시그널
        self.dial.valueChanged.connect(self.Dial_Changed)

        self.vbox = QVBoxLayout(self)        
        self.vbox.addWidget(self.dial)
        self.vbox.addWidget(self.label)

        self.show()
    
    def Dial_Changed(self):
        self.label.setText(str(self.dial.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()
    app.exec_()