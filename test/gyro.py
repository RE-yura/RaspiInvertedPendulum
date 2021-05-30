# -*- coding: utf-8 -*-

import smbus
import math
from time import sleep
import time
import numpy as np
# import matplotlib.pyplot as plt

class Gyro():
    
    def __init__(self):
        self.DEV_ADDR = 0x68
        self.ACCEL_OUT = [0x3b, 0x3d,0x3f]
        self.GYRO_OUT = [0x43, 0x45, 0x47]

        self.gr = [0, 0, 0]
        self.ac = [0, 0, 0]
        self.angle = 0.0

        self.PWR_MGMT_1 = 0x6b

    def read_word(self, adr):
        smbus.SMBus(1).write_byte_data(self.DEV_ADDR, self.PWR_MGMT_1, 0)
        high = smbus.SMBus(1).read_byte_data(self.DEV_ADDR, adr)
        low = smbus.SMBus(1).read_byte_data(self.DEV_ADDR, adr+1)
        val = (high << 8) + low
        return val

    def read_word_sensor(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):  return -((65535 - val) + 1)
        else:  return val

    def getGyro(self):
        for j in range(3):
            self.gr[j] = self.read_word_sensor(self.GYRO_OUT[j])/ 16384.0

    def getAccel(self):
        for j in range(3):
            self.ac[j] = self.read_word_sensor(self.ACCEL_OUT[j])/ 16384.0

    def getAngle(self):
            self.angle = np.arctan2(
                self.ac[2], self.ac[1]) * 180 / 3.141592



def main():
    #=======初期設定===================================
    gyro = Gyro()
    #==================================================

    try:
        while 1:
            gyro.getAccel()
            gyro.getGyro()
            gyro.getAngle()

            # print ('{0:4.3f},   {0:4.3f},    {0:4.3f},     {0:4.3f},      {0:4.3f},      {0:4.3f},' .format(gyro.gr[0], gyro.gr[1], gyro.gr[2], gyro.ac[0], gyro.ac[1], gyro.ac[2]))

            print ('{0:4.3f}' .format(gyro.angle))


    except KeyboardInterrupt:
        print ("while_break")
        
     
if __name__ == "__main__":   
    main()