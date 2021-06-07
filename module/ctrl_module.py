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

    def getGain(self):
        # GainParam.txtからゲイン取得
        arrayFlo = [[0] * 3] * 2
        arrayStr = self.file.ReadList()
        for i in range(len(arrayStr)):
            arrayFlo[i] = [float(j) for j in arrayStr[i]]
        self.unit.setGain(arrayFlo[0])
        # print(arrayFlo[0])

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
            mode = ctrl.client.receiveStr()

            # フラグ取得
            if not mode == None:
                if mode == "Run":
                    flag = 1
                    ctrl.getGain()
                elif mode == "Stop":
                    flag = 2

                elif mode == "Init":
                    ctrl.unit.gyro.setAngleoffset(ctrl.unit.gyro.angle_row)

                elif mode == "Close":
                    ctrl.unit.drive(ctrl.unit.ACT_FORWARD, 0)
                    break

                elif 'Change' in mode:
                    Carray = mode.split(" ")
                    print(float(Carray[1]))
                    pass


            # 車体動作
            if flag == 1:
                # ctrl.unit.drive(ctrl.unit.ACT_FORWARD,10)
                ctrl.unit.position_control()
                print(ctrl.unit.gyro.angle)
            elif flag == 2:
                ctrl.unit.drive(ctrl.unit.ACT_FORWARD, 0)
                ctrl.unit.gyro.getAccel()
                ctrl.unit.gyro.getAngle()
            else:
                ctrl.unit.gyro.getAccel()
                ctrl.unit.gyro.getAngle()
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    del ctrl


if __name__ == "__main__":
    main()
