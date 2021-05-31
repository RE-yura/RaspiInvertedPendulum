import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subwindow import *
from server import *
import pyautogui
import socket


class MainWindow(QWidget):
    server = Server()
    def __init__(self):
        super().__init__()


        layout = QGridLayout()

        StartButton = QPushButton("Run", self)
        StartButton.clicked.connect(self.RunMode)
        layout.addWidget(StartButton, 0, 0)

        StopButton = QPushButton("Stop", self)
        StopButton.clicked.connect(self.StopMode)
        layout.addWidget(StopButton, 0, 1)

        makeWindowButton = QPushButton("Gain", self)
        makeWindowButton.clicked.connect(self.makeWindow)
        layout.addWidget(makeWindowButton, 1, 0)

        CloseButton = QPushButton("Close", self)        
        CloseButton.clicked.connect(self.close)
        layout.addWidget(CloseButton, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle('InvertedPendulum')
        self.setGeometry(300, 300, 300, 100)


    def makeWindow(self):
        subWindow = SubWindow(self)
        subWindow.show()
    
    def RunMode(self):
        self.server.sendUDP("Run")

    def StopMode(self):
        self.server.sendUDP("Stop")


if __name__ == '__main__':
    # シンプルコマンド
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
