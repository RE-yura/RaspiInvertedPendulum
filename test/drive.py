import RPi.GPIO as GPIO
import wiringpi as pi
import time
import enum as Enum
from Encorder import *
from gyro import *
import signal

import sys, os
sys.path.append(os.path.join('..', 'gui'))
from client import *


class Motor(Enum):
    RIGHT = 0
    LEFT = 1

class Gnum():
    P = 0
    D = 1
    I = 2

class DriveUnit():

    def __init__(self, Glist):
        self.ACT_FORWARD = 0
        self.ACT_BACKWARD = 1
        self.ACT_BREAK = 2
        self.ACT_STOP = 3


        self.Angle_offset = 0

        self.lastErr = 0

        self.UMAX = 100
        self.errP = 0
        self.errD = 0
        self.errI = 0
        self.gainP = 0
        self.gainD = 0
        self.gainI = 0.5
        self.exu = 0
        self.u = 0

        self.ANG_VELO = 780     #角速度±780dps
        self.dt = 0
        self.now = 0
        self.preTime = time.time()

        #インスタンス生成
        self.gyro = Gyro()
        self.motorR = EncoderedMotor(Gear.MOTOR_GEAR_1, PinType.ENCORDER_1A, PinType.ENCORDER_1B, PinType.MOTOR_1A, PinType.MOTOR_1B)
        self.motorL = EncoderedMotor(Gear.MOTOR_GEAR_2, PinType.ENCORDER_2A, PinType.ENCORDER_2B, PinType.MOTOR_2A, PinType.MOTOR_2B)

        #ゲイン登録
        self.setGain(Glist)
    
    
    def drive(self, dir, pwm):
        #車体移動
        if dir == self.ACT_FORWARD:
            self.motorR.motor_ctrl(DriveType.ROT_RIGHT,abs(pwm))
            self.motorL.motor_ctrl(DriveType.ROT_LEFT,abs(pwm))
        elif dir == self.ACT_BACKWARD:
            self.motorR.motor_ctrl(DriveType.ROT_LEFT,abs(pwm))
            self.motorL.motor_ctrl(DriveType.ROT_RIGHT,abs(pwm))

    def calc_dt(self):        
        self.now = time.time()
        self.dt = (self.now - self.preTime)
        self.preTime = self.now

    def calc_errp(self):   
        self.errP = (self.gyro.angle / 90.0 - 1) * self.UMAX  # P成分：傾き-180～0度 → -100～100

        if abs(self.errP) < 0.1:
            self.errP = 0



    def calc_errd(self):
        self.errD = (self.errP - self.lastErr) / self.dt / self.ANG_VELO * self.UMAX  # D成分：角速度±780dps → -100～100
        if abs(self.errD) < 10:
            self.errD = 0
        self.lastErr = self.errP

    
    
    def calc_erri(self):
        self.errI += self.errP * self.dt  # I成分


    def position_control(self):
        self.gyro.getAccel()
        self.gyro.getGyro()
        self.gyro.getAngle()

        #dt計算
        self.calc_dt()
        
        #偏差計算
        self.calc_errp()
        self.calc_errd()
        self.calc_erri()
        

        #PWM計算
        self.u = self.exu * self.u + (1 - self.exu) * (self.gainP * self.errP + self.gainD * self.errD + self.gainI * self.errI) 
        
        if self.u > 100:
            self.u = 100
        elif self.u < -100:
            self.u = -100

        #モーター駆動
        self.balance()


    def setGain(self, Glist):
        self.gainP = Glist[0]
        self.gainD = Glist[1]
        self.gainI = Glist[2]


    def balance(self):
        if self.u > 0:
            self.drive(self.ACT_FORWARD, self.u)
        else:
            self.drive(self.ACT_BACKWARD, self.u)

    def __del__(self):
        del self.gyro
        del self.motorR
        del self.motorL



def main():
    try:
        #=======初期設定===================================
        unit = DriveUnit([10, 0, 0])
        gyro = Gyro()
        # unit = DriveUnit(0, 1200, 0)
        #==================================================

        while True:
            # unit.drive(unit.ACT_BACKWARD, 10)
            unit.position_control()
            print ('{0:4.2f}' .format(unit.gyro.angle))
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    del unit
if __name__ == "__main__":   
    main()