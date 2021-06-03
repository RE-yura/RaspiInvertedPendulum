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


class Direction(Enum):
    forward = 0
    backward = 1

class Motor(Enum):
    right = 0
    left = 1

class Gnum():
    P = 0
    D = 1
    I = 2

class DriveUnit():
    gyro = Gyro()

    def __init__(self, Glist):
        self.lastErr = 0
        self.err = [0]*3
        self.gain = [0]*3

        self.dt = 0
        self.now = 0
        self.preTime = time.time()

        self.motorR = EncoderedMotor(Gear.MOTOR_GEAR_1, PinType.ENCORDER_1A, PinType.ENCORDER_1B, PinType.MOTOR_1A, PinType.MOTOR_1B)#インスタンス生成

        self.motorL = EncoderedMotor(Gear.MOTOR_GEAR_2, PinType.ENCORDER_2A, PinType.ENCORDER_2B, PinType.MOTOR_2A, PinType.MOTOR_2B)#インスタンス生成

        signal.signal(signal.SIGALRM, self.intervalHandler)
        signal.setitimer(signal.ITIMER_REAL, 0.01, 0.02)

        self.setPID(Glist)
        

   
    def intervalHandler(self, signum, frame):
        self.gyro.getAccel()
        self.gyro.getGyro()
        self.gyro.getAngle()
        self.motorR.encorder2angle()
        self.motorL.encorder2angle()
    
    
    def drive(self, dir, pwm):
        if dir == Direction.forward:
            self.motorR.motor_ctrl(DriveType.ROT_RIGHT,abs(pwm))
            self.motorL.motor_ctrl(DriveType.ROT_LEFT,abs(pwm))
        elif dir == Direction.backward:
            self.motorR.motor_ctrl(DriveType.ROT_LEFT,abs(pwm))
            self.motorL.motor_ctrl(DriveType.ROT_RIGHT,abs(pwm))

    def calc_dt(self):        
        self.now = time.time()
        self.dt = (self.now - self.preTime)
        self.preTime = self.now

    def calc_errp(self):   
        self.err[Gnum.P] = self.gyro.angle / 90.0 - 1  # P成分：傾き-180～0度 → -1～1
        # print(self.gyro.angle)


    def calc_errd(self):
        self.err[Gnum.D] = (self.err[Gnum.P] - self.lastErr) / self.dt / 780.0  # D成分：角速度±780dps → -1～1
        self.lastErr = self.err[Gnum.P]
    
    def calc_erri(self):
        self.err[Gnum.I] += self.err[Gnum.P] * self.dt  # I成分

    def position_control(self):
        self.calc_dt()
        self.calc_errp()
        self.calc_errd()
        self.calc_erri()
        self.u = 0
        for i in range(3):
            self.u += self.gain[i] * self.err[i]
        self.balance()


    def setPID(self, Glist):
        self.gain = Glist


    def balance(self):
        if self.u < 0:
            self.drive(Direction.forward, self.u)
        elif self.u > 0:
            self.drive(Direction.backward, self.u)
                        
    # def Gyro2Motor(self):
    #     if self.gyro.angle > 0:
    #         self.drive(Direction.forward, int(self.gyro.angle/2))
    #     else:
    #         self.drive(Direction.backward,-int(self.gyro.angle/2))

    def __del__(self):
        del self.motorR
        del self.motorL
    



def main():
    #=======初期設定===================================
    unit = DriveUnit([80, 0, 0])
    # unit = DriveUnit(0, 1200, 0)
    client = Client()
    #==================================================
    count = 0
    while True:
        try:

            # unit.drive(Direction.backward, 10)
            # unit.Gyro2Motor()
            unit.position_control()
            print(unit.gyro.angle)            

            time.sleep(0.001)

        
        # except IOError:
        #     print("IOError")
        #     pass

        except KeyboardInterrupt:
            del unit
 
if __name__ == "__main__":   
    main()