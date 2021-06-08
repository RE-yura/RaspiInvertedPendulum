# -*- coding: utf-8 -*-

import smbus
from time import sleep
import numpy as np


class Gyro():

    def __init__(self):
        self.DEV_ADDR = 0x68
        self.ACCEL_OUT = [0x3b, 0x3d, 0x3f]
        self.GYRO_OUT = [0x43, 0x45, 0x47]

        self.gr = [0, 0, 0]
        self.ac = [0, 0, 0]
        self.angle_row = 0.0
        self.angle_accel = 0.0
        self.angle = 0.0
        self.angle_offset = 0.0
        self.CF = 0.995

        self.PWR_MGMT_1 = 0x6b
        # signal.signal(signal.SIGALRM, self.intervalHandler)
        # signal.setitimer(signal.ITIMER_REAL, 0.2, 0.1)

    def read_word(self, adr):
        smbus.SMBus(1).write_byte_data(self.DEV_ADDR, self.PWR_MGMT_1, 0)
        high = smbus.SMBus(1).read_byte_data(self.DEV_ADDR, adr)
        low = smbus.SMBus(1).read_byte_data(self.DEV_ADDR, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_sensor(self, adr):
        val = self.read_word(adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def set_angle_offset(self):
        self.angle_offset = self.angle_row - 90.0

    def get_gyro(self):
        for j in range(3):
            self.gr[j] = self.read_word_sensor(self.GYRO_OUT[j]) / 16384.0
        # print("gyro")

    def get_accel(self):
        for j in range(3):
            self.ac[j] = self.read_word_sensor(self.ACCEL_OUT[j]) / 16384.0

    def get_angle(self):
        self.angle_row = np.arctan2(
            self.ac[2], self.ac[0]) * 180 / 3.141592
        self.angle_accel = self.angle_row - self.angle_offset
        self.angle = self.CF * (self.angle + self.gr[1]) + (1 - self.CF) * self.angle_accel
        # self.angle = self.CF * self.angle  + (1 - self.CF) * self.angle_accel
        # self.angle =  self.angle_accel

        # print("Angle:",self.angle,"     gyro:", self.gr[1])


def main():
    try:
        # =======初期設定===================================
        gyro = Gyro()
        # ==================================================

        while True:
            gyro.get_accel()
            gyro.get_gyro()
            gyro.get_angle()
            print('{0:4.3f}' .format(gyro.angle))
            sleep(0.1)
            # print ('{0:4.3f},   {0:4.3f},    {0:4.3f},     {0:4.3f},      {0:4.3f},      {0:4.3f},' .format(gyro.gr[0], gyro.gr[1], gyro.gr[2], gyro.ac[0], gyro.ac[1], gyro.ac[2]))

    except KeyboardInterrupt:
        print("while_break")


if __name__ == "__main__":
    main()
