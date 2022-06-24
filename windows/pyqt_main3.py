## QFont 속성
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont # 위젯x 속성
from PyQt5.QtCore import Qt # Core속성

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 내가 만들 UI 초기화 함수

    def initUI(self):
        self.setWindowTitle('QFont test')
        self.setGeometry(490, 250, 300, 300)
        self.text = 'What the F*!!'
        self.show()

    def paintEvent(self, signal):
        paint = QPainter(self)
        paint.begin(self)
        self.drawText(signal, paint)
        paint.end()
    
    def drawText(self, signal, paint):
        paint.setPen(QColor(100,100,255)) # R,G,B 0~255
        paint.setFont(QFont('Impact', 20))
        paint.drawText(105, 100, 'Hell World!')
        paint.setPen(QColor(100,100,100))
        paint.setFont(QFont('Arial', 16))
        paint.drawText(signal.rect(), Qt.AlignCenter, self.text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()