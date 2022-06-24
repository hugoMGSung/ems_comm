## QSlider, QDial
import sys
from PyQt5.QtWidgets import * # All
from PyQt5.QtGui import * # All
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 내가 만들 UI 초기화 함수

    def initUI(self):
        self.setWindowTitle('QSlider&QDial')
        self.setGeometry(490, 250, 300, 390)
        self.setWindowIcon(QIcon('lion.png'))

        # 슬라이더
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 50)
        self.slider.setSingleStep(2)
        self.slider.setTickPosition(3)

        # 다이얼
        self.dial = QDial(self)
        self.dial.setRange(0, 50)
        self.dial.setSingleStep(2)        

        self.btn = QPushButton('Reset', self)

        # 시그널 정의
        self.slider.valueChanged.connect(self.slider_changed)
        self.dial.valueChanged.connect(self.dial_changed)
        self.btn.clicked.connect(self.btn_clicked)

        # 화면 구성        
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.slider)
        vbox.addWidget(self.dial)
        vbox.addWidget(self.btn)

        self.show()

    def slider_changed(self):
        val = self.slider.value()
        self.dial.setValue(val)

    def dial_changed(self):
        val = self.dial.value()
        self.slider.setValue(val)

    def btn_clicked(self):
        self.slider.setValue(0)
        self.dial.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()