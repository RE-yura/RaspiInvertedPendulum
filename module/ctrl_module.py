import time
import RPi.GPIO as GPIO
from drive import *
import sys
import os


sys.path.append(os.path.join('..', 'gui'))
from client import *
from file import *


class Ctrl():
    def __init__(self):
        # インスタンス生成
        self.unit = DriveUnit([80, 0, 0])
        self.client = Client()
        self.file = FileOp()

    def get_gain(self):
        # GainParam.txtからゲイン取得
        array_flo = [[0] * 3] * 2
        array_str = self.file.read_list()
        for i in range(len(array_str)):
            array_flo[i] = [float(j) for j in array_str[i]]
        self.unit.set_gain(array_flo[0])
        # print(array_flo[0])

    def __del__(self):
        del self.unit
        del self.client
        del self.file


def main():

    flag = 0
    try:
        # =======初期設定===================================
        ctrl = Ctrl()
        # ==================================================
        while True:
            # UDP通信でmode取得
            mode = ctrl.client.receive_str()

            # フラグ取得
            if not mode == None:
                if mode == "Run":
                    flag = 1
                    ctrl.get_gain()
                elif mode == "Stop":
                    flag = 2

                elif mode == "Init":
                    
                    ctrl.unit.gyro.set_angle_offset()

                elif mode == "Close":
                    ctrl.unit.drive(ctrl.unit.ACT_FORWARD, 0)
                    break

                elif 'Change' in mode:
                    c_array = mode.split(" ")
                    ctrl.unit.gyro.angle_offset += float(c_array[1])
                    print(float(c_array[1]))


            # 車体動作
            if flag == 1:
                # ctrl.unit.drive(ctrl.unit.ACT_FORWARD,10)
                ctrl.unit.position_control()
            elif flag == 2:
                ctrl.unit.drive(ctrl.unit.ACT_FORWARD, 0)
                ctrl.unit.gyro.get_accel()
                ctrl.unit.gyro.get_angle()
            else:
                ctrl.unit.gyro.get_accel()
                ctrl.unit.gyro.get_angle()
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    del ctrl


if __name__ == "__main__":
    main()
