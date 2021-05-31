import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subwindow import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        makeWindowButton = QPushButton("setGain", self)
        makeWindowButton.move(150, 50)
        makeWindowButton.clicked.connect(self.makeWindow)

        self.setWindowTitle('InvertedPendulum')
        self.setGeometry(300, 300, 400, 100)

    def makeWindow(self):
        subWindow = SubWindow(self)
        subWindow.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
