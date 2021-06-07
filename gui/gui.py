import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subwindow import *
from server import *


class MainWindow(QWidget):
    server = Server()

    def __init__(self):
        super().__init__()

        self.file = FileOp()

        layout = QGridLayout()

        StartButton = QPushButton("Run", self)
        StartButton.clicked.connect(self.RunMode)
        layout.addWidget(StartButton, 0, 0)

        StopButton = QPushButton("Stop", self)
        StopButton.clicked.connect(self.StopMode)
        layout.addWidget(StopButton, 0, 1)

        spb = QSpinBox()

        # 水平方向のスライダー作成
        self.sld = QSlider(Qt.Vertical, self)
        self.sld.setRange(-100, 100)
        self.sld.setValue(0)
        # スライダーがフォーカスされないようにする
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.valueChanged[int].connect(self.sliderChangeValue)
        layout.addWidget(self.sld, 0, 3, 3, 1)

        initAngleButton = QPushButton("Init", self)
        initAngleButton.clicked.connect(self.initAngle)
        layout.addWidget(initAngleButton, 1, 0)

        initAngleButton = QPushButton("Reset", self)
        initAngleButton.clicked.connect(self.resetAngle)
        layout.addWidget(initAngleButton, 1, 1)

        makeWindowButton = QPushButton("Gain", self)
        makeWindowButton.clicked.connect(self.makeWindow)
        layout.addWidget(makeWindowButton, 2, 0)

        CloseButton = QPushButton("Close", self)
        CloseButton.clicked.connect(self.closeWindow)
        # CloseButton.clicked.connect(self.close)
        layout.addWidget(CloseButton, 2, 1)
        self.setLayout(layout)

        self.setWindowTitle('InvertedPendulum')
        self.setGeometry(300, 300, 300, 100)

    def makeWindow(self):
        subWindow = SubWindow(self)
        subWindow.show()

    def RunMode(self):
        arrayFlo = [[0] * 3] * 2
        arrayStr = self.file.ReadList()
        for i in range(len(arrayStr)):
            arrayFlo[i] = [float(j) for j in arrayStr[i]]
        # print(arrayFlo)
        self.server.sendStr("Run")

    def closeWindow(self):
        self.server.sendStr("Close")
        self.close()

    def resetAngle(self):
        self.sld.setValue(0)
        self.server.sendStr("Reset")

    def initAngle(self):
        self.sld.setValue(0)
        self.server.sendStr("Init")

    def StopMode(self):
        self.server.sendStr("Stop")

    def sliderChangeValue(self, value):
        # """ Slider の値が変わった時に呼ばれる処理 """
        self.server.sendStr("Change "+str(self.sld.value()))
        
        # self.spb[i].setValue(sld.value())
        # self.updateColor()
        pass

if __name__ == '__main__':
    # シンプルコマンド
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
