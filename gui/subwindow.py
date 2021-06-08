# !/usr/bin/python3
# -*- coding: utf-8 -*-
# import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from file import *


class SubWindow:
    def __init__(self, parent=None):
        self.w = QDialog(parent)
        self.parent = parent
        self.file = FileOp()
        pre_data = self.file.read_list()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.regParam)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.w.close)
        # 水平なボックスを作成
        hbox = QHBoxLayout()
        # ボタンの大きさが変わらないようにする
        # ボタンの左側に水平方向に伸縮可能なスペースができるため、ボタンは右に寄る
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        self.gain_list = [[0 for _ in range(3)] for _ in range(2)]
        print(pre_data)
        gain_box = QVBoxLayout()
        for i in range(2):
            gain_hbox = QHBoxLayout()
            for j in range(3):
                if len(pre_data) == 2 and len(pre_data[0]) == 3:
                    self.gain_list[i][j] = QLineEdit(pre_data[i][j])
                else:
                    self.gain_list[i][j] = QLineEdit("0.0")
                self.gain_list[i][j].setValidator(QDoubleValidator())
                gain_hbox.addWidget(self.gain_list[i][j])
            gain_box.addLayout(gain_hbox)

        # 垂直なボックスを作成
        vbox = QVBoxLayout()
        vbox.addLayout(gain_box)
        # 垂直方向に伸縮可能なスペースを作る

        vbox.addStretch(1)
        # 右下にボタンが移る
        vbox.addLayout(hbox)

        # 画面に上で設定したレイアウトを加える
        self.w.setLayout(vbox)

    def show(self):
        self.w.exec_()

    def regParam(self):
        self.file.reset_char()
        for i in range(2):
            print([j.text() for j in self.gain_list[i]])
            self.file.write_list([j.text() for j in self.gain_list[i]])

        self.w.close()
