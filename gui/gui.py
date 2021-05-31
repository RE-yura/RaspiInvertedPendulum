#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # OKボタンとCancelボタンの作成
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.getParam)

        cancelButton = QPushButton("Cancel")

        # 水平なボックスを作成
        hbox = QHBoxLayout()
        # ボタンの大きさが変わらないようにする
        # ボタンの左側に水平方向に伸縮可能なスペースができるため、ボタンは右に寄る
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        self.gain_list = [[0 for _ in range(3)] for _ in range(2)]

        GainVBox = QVBoxLayout()
        for i in range(2):
            GainHBox = QHBoxLayout()
            for j in range(3):
                self.gain_list[i][j] = QLineEdit(self)
                # self.gain_list[i][j].setValidator()
                self.gain_list[i][j].setValidator(QDoubleValidator())
                GainHBox.addWidget(self.gain_list[i][j])
            GainVBox.addLayout(GainHBox)

        # 垂直なボックスを作成
        vbox = QVBoxLayout()
        vbox.addLayout(GainVBox)
        # 垂直方向に伸縮可能なスペースを作る

        vbox.addStretch(1)
        # 右下にボタンが移る
        vbox.addLayout(hbox)

        # 画面に上で設定したレイアウトを加える
        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Gain Adjustment')
        self.show()

    def getParam(self):
        for i in range(2):
            print([j.text() for j in self.gain_list[i]])


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
