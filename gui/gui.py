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
        self.ANGLE_CONST = 200
        self.val_sum = 0

        self.file = FileOp()

        layout = QGridLayout()

        StartButton = QPushButton("Run", self)
        StartButton.clicked.connect(self.run_mode)
        layout.addWidget(StartButton, 0, 0)

        StopButton = QPushButton("Stop", self)
        StopButton.clicked.connect(self.stop_mode)
        layout.addWidget(StopButton, 0, 1)

        # 水平方向のスライダー作成
        self.sld = QSlider(Qt.Vertical, self)
        self.sld.setRange(-100, 100)
        self.sld.setValue(0)
        # スライダーがフォーカスされないようにする
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.valueChanged[int].connect(self.slider_change_value)
        layout.addWidget(self.sld, 0, 3, 3, 1)

        init_angle_button = QPushButton("Init", self)
        init_angle_button.clicked.connect(self.init_angle)
        layout.addWidget(init_angle_button, 1, 0)

        init_angle_button = QPushButton("Reset", self)
        init_angle_button.clicked.connect(self.reset_angle)
        layout.addWidget(init_angle_button, 1, 1)

        makeWindowButton = QPushButton("Gain", self)
        makeWindowButton.clicked.connect(self.make_window)
        layout.addWidget(makeWindowButton, 2, 0)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.clode_window)
        # close_button.clicked.connect(self.close)
        layout.addWidget(close_button, 2, 1)
        self.setLayout(layout)

        self.setWindowTitle('InvertedPendulum')
        self.setGeometry(300, 300, 300, 100)

    def make_window(self):
        subWindow = SubWindow(self)
        subWindow.show()

    def run_mode(self):
        array_flo = [[0] * 3] * 2
        array_str = self.file.read_list()
        for i in range(len(array_str)):
            array_flo[i] = [float(j) for j in array_str[i]]
        # print(array_flo)
        self.server.send_str("Run")

    def clode_window(self):
        self.server.send_str("Close")
        self.close()

    def reset_angle(self):
        self.sld.setValue(0)
        self.server.send_str("Reset")

    def init_angle(self):
        self.val_sum += self.sld.value() / self.ANGLE_CONST
        self.sld.setValue(0)
        self.server.send_str("Init")

    def stop_mode(self):
        self.server.send_str("Stop")

    def slider_change_value(self, value):
        # """ Slider の値が変わった時に呼ばれる処理 """
        angle_val = self.sld.value() / self.ANGLE_CONST + self.val_sum
        self.server.send_str("Change "+str(angle_val))

if __name__ == '__main__':
    # シンプルコマンド
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
