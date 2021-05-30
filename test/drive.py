import RPi.GPIO as GPIO
import wiringpi as pi
import time
import enum as Enum
from Encorder import *
from gyro import *


class Direction(Enum):
    forward = 0
    backward = 1
 
class DriveUnit():
    def __init__(self):
        self.motorR = EncoderedMotor(Gear.MOTOR_GEAR_1, PinType.ENCORDER_1A, PinType.ENCORDER_1B, PinType.MOTOR_1A, PinType.MOTOR_1B)#インスタンス生成

        self.motorL = EncoderedMotor(Gear.MOTOR_GEAR_2, PinType.ENCORDER_2A, PinType.ENCORDER_2B, PinType.MOTOR_2A, PinType.MOTOR_2B)#インスタンス生成

    def drive(self, dir, pwm):
        if dir == Direction.forward:
            self.motorR.motor_ctrl(DriveType.ROT_RIGHT,pwm)
            self.motorL.motor_ctrl(DriveType.ROT_LEFT,pwm)
        elif dir == Direction.backward:
            self.motorR.motor_ctrl(DriveType.ROT_LEFT,pwm)
            self.motorL.motor_ctrl(DriveType.ROT_RIGHT,pwm)
                        
    def __del__(self):
        del self.motorR
        del self.motorL



def main():
    #=======初期設定===================================
    unit = DriveUnit()
    #==================================================

    try:
        while(True):
            unit.drive(Direction.backward, 10)
            time.sleep(0.1)


    except KeyboardInterrupt:
        del drive
 
if __name__ == "__main__":   
    main()