## QPushButton
import sys
from PyQt5.QtWidgets import * # All
from PyQt5.QtGui import * # All
from PyQt5.QtCore import *

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 내가 만들 UI 초기화 함수

    def initUI(self):
        self.setWindowTitle('QPushButton')
        self.setGeometry(490, 250, 300, 300)
        self.setWindowIcon(QIcon('lion.png'))

        btn1 = QPushButton('Hello', self)
        # btn1.setEnabled(True)
        btn1.clicked.connect(self.btn1_click) # 시그널

        vbox = QVBoxLayout(self)
        vbox.addWidget(btn1)

        self.show()

    def btn1_click(self): # 슬롯
        QMessageBox.about(self, 'greeting', 'Hi, everyone~')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()