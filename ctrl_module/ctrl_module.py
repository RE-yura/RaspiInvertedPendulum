import RPi.GPIO as GPIO
import wiringpi as pi
import time
import enum as Enum
import signal

import sys, os
sys.path.append(os.path.join('..', 'gui'))
sys.path.append(os.path.join('..', 'test'))
# import drive
# import gui
# import client
from drive import *
# from gui import *
from client import *
from file import *


class Ctrl():
    def __init__(self):
        self.unit = DriveUnit([80, 0, 0])
        self.client = Client()
        self.file = FileOp()

    def getGain(self):
        arrayFlo = [[0]*3]*2
        arrayStr = self.file.ReadList()
        for i in range(len(arrayStr)):
            arrayFlo[i] = [float(j) for j in arrayStr[i]]
        self.unit.setPID(arrayFlo[0])
        print(arrayFlo[0])
        



def main():
    # pass
    #=======初期設定===================================
    ctrl = Ctrl()
    # unit = DriveUnit(20, 0, 0)
    # client = Client()
    # file = FileOp()
    #==================================================
    flag = 0
    count = 0
    while True:
        pass
        try:
            mode = ctrl.client.receiveStr()
            if mode == "Run":
                flag = 1
                ctrl.getGain()

            if mode == "Stop":
                flag = 2        

            if flag == 1:
                ctrl.unit.position_control()
                # print(ctrl.unit.gyro.angle)
            elif flag == 2:
                pass

            time.sleep(0.01)

        
        # except IOError:
        #     print("IOError")
        #     pass

        except KeyboardInterrupt:
            del ctrl
 
if __name__ == "__main__":   
    main()