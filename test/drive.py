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
        self.FORWARD = 0
        self.BACKWARD = 1
        self.BREAK = 2
        self.STOP = 3


        self.Angle_offset = 0

        self.lastErr = 0
        self.err = [0]*3
        self.gain = [0]*3
        self.ANG_VELO = 780     #角速度±780dps
        self.dt = 0
        self.now = 0
        self.preTime = time.time()

        #インスタンス生成
        self.gyro = Gyro()
        self.motorR = EncoderedMotor(Gear.MOTOR_GEAR_1, PinType.ENCORDER_1A, PinType.ENCORDER_1B, PinType.MOTOR_1A, PinType.MOTOR_1B)
        self.motorL = EncoderedMotor(Gear.MOTOR_GEAR_2, PinType.ENCORDER_2A, PinType.ENCORDER_2B, PinType.MOTOR_2A, PinType.MOTOR_2B)

        # #割り込み処理登録(始動delay, 始動間隔)
        # signal.signal(signal.SIGALRM, self.intervalHandler)
        # signal.setitimer(signal.ITIMER_REAL, 0.01, 0.02)

        #ゲイン登録
        self.setGain(Glist)
        

   
    # def intervalHandler(self, signum, frame):
        #割り込み処理する関数
        # self.gyro.getAccel()
        # self.gyro.getGyro()
        # self.gyro.getAngle()
        # self.motorR.encorder2angle()
        # self.motorL.encorder2angle()
    
    
    def drive(self, dir, pwm):
        #車体移動
        if dir == self.FORWARD:
            self.motorR.motor_ctrl(DriveType.ROT_RIGHT,abs(pwm))
            self.motorL.motor_ctrl(DriveType.ROT_LEFT,abs(pwm))
        elif dir == self.BACKWARD:
            self.motorR.motor_ctrl(DriveType.ROT_LEFT,abs(pwm))
            self.motorL.motor_ctrl(DriveType.ROT_RIGHT,abs(pwm))

    def calc_dt(self):        
        self.now = time.time()
        self.dt = (self.now - self.preTime)
        self.preTime = self.now

    def calc_errp(self):   
        self.err[Gnum.P] = self.gyro.angle / 90.0 - 1  # P成分：傾き-180～0度 → -1～1


    def calc_errd(self):
        self.err[Gnum.D] = (self.err[Gnum.P] - self.lastErr) / self.dt / self.ANG_VELO  # D成分：角速度±780dps → -1～1
        self.lastErr = self.err[Gnum.P]
    
    def calc_erri(self):
        self.err[Gnum.I] += self.err[Gnum.P] * self.dt  # I成分


    def position_control(self):
        self.gyro.getAccel()
        self.gyro.getAngle()

        #dt計算
        self.calc_dt()
        
        #偏差計算
        self.calc_errp()
        self.calc_errd()
        self.calc_erri()
        

        #PWM計算
        self.u = 0
        for i in range(3):
            self.u += self.gain[i] * self.err[i]
        
        #モーター駆動
        self.balance()


    def setGain(self, Glist):
        self.gain = Glist


    def balance(self):
        if self.u > 0:
            self.drive(self.FORWARD, self.u)
        elif self.u < 0:
            self.drive(self.BACKWARD, self.u)
                        

    def __del__(self):
        del self.gyro
        del self.motorR
        del self.motorL



def main():
    try:
        #=======初期設定===================================
        unit = DriveUnit([80, 0, 0])
        gyro = Gyro()
        # unit = DriveUnit(0, 1200, 0)
        #==================================================

        while True:
            # unit.drive(unit.BACKWARD, 10)
            unit.position_control()
            # print ('{0:4.2f}' .format(unit.gyro.angle))
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    del unit
if __name__ == "__main__":   
    main()