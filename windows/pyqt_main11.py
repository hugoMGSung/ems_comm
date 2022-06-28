# QtDesinger 연동
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/testwin.ui', self)

        self.dial.valueChanged.connect(self.dial_Changed)
        self.show()

    def dial_Changed(self):
        self.label.setText(str(self.dial.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()


