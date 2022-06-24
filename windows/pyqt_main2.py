## PyQt 클래스화 / PyQt 템플릿
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 내가 만들 UI 초기화 함수

    def initUI(self):
        self.setWindowTitle('PyQt Widget2')
        # self.move(490, 250) # x=(1280/2)-(300/2), y=(800/2)-(300/2)
        # self.resize(300, 300)
        self.setGeometry(490, 250, 300, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()