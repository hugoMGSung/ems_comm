# Custom Signal&Slot
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QWidget): # QMainWindow로 변경요
    closeSignal = pyqtSignal() # 커스텀시그널

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Close Demo')
        self.resize(300, 300)

        self.btnClose = QPushButton('close', self)
        self.btnClose.clicked.connect(self.btnCloseClicked)
        self.closeSignal.connect(self.onClose)

        # TODO 로직은 여기에 작성        
        self.show()
    
    def btnCloseClicked(self):
        self.closeSignal.emit()

    def onClose(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()