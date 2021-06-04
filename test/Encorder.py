import RPi.GPIO as GPIO
import wiringpi as pi
import time
from enum import Enum
from gyro import *

class DriveType(Enum):
    ROT_RIGHT = 1
    ROT_LEFT = 2

class PinType(): 
    ENCORDER_1A = 17
    ENCORDER_1B = 27
    ENCORDER_2A = 5
    ENCORDER_2B = 6
    
    MOTOR_1A = 23
    MOTOR_1B = 24
    MOTOR_2A = 25
    MOTOR_2B = 8

class Gear():
    MOTOR_GEAR_1 = 1970   #ざっとキャリブレーション
    MOTOR_GEAR_2 = 1970   #ざっとキャリブレーション

class EncoderedMotor():
    def __init__(self, gears, ENCORDER_PIN_A, ENCORDER_PIN_B,  MOTOR_PIN_A, MOTOR_PIN_B):
        self.angle = 0 
        self.prev_data = 0
        self.setDelta(gears)
        self.setEncorderPin(ENCORDER_PIN_A, ENCORDER_PIN_B)
        self.setMotorPin(MOTOR_PIN_A, MOTOR_PIN_B)
        self.setup()
        self.gyro = Gyro()

        #callback登録
        GPIO.add_event_detect(self.IN_ENCORDER_PIN_A, GPIO.BOTH, callback=self.callback)
        GPIO.add_event_detect(self.IN_ENCORDER_PIN_B, GPIO.BOTH, callback=self.callback)

    def setDelta(self, gears):
        self.delta = 360./gears

    def setEncorderPin(self, ENCORDER_PIN_A, ENCORDER_PIN_B):
        #エンコーダーピン配置
        self.IN_ENCORDER_PIN_A = ENCORDER_PIN_A
        self.IN_ENCORDER_PIN_B = ENCORDER_PIN_B

    def setMotorPin(self, MOTOR_PIN_A, MOTOR_PIN_B):
        #モーターピン配置
        self.IN_MOTOR_PIN_A = MOTOR_PIN_A
        self.IN_MOTOR_PIN_B = MOTOR_PIN_B

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        #エンコーダー立ち上げ
        GPIO.setup(self.IN_ENCORDER_PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_ENCORDER_PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)    

        #モーター立ち上げ
        pi.wiringPiSetupGpio()
        pi.pinMode( self.IN_MOTOR_PIN_A, pi.OUTPUT )
        pi.pinMode( self.IN_MOTOR_PIN_B, pi.OUTPUT )

        # モータードライバを接続したGPIOをPWM出力できるようにする
        pi.softPwmCreate( self.IN_MOTOR_PIN_A, 0, 100 )
        pi.softPwmCreate( self.IN_MOTOR_PIN_B, 0, 100 )  


        # モーターの初期状態
        pi.softPwmWrite( self.IN_MOTOR_PIN_A, 0 )
        pi.softPwmWrite( self.IN_MOTOR_PIN_B, 0 )
        
    def motor_ctrl(self, TYPE, pwm):
        if TYPE == DriveType.ROT_RIGHT:     #モータ反動あり
            pi.softPwmWrite( self.IN_MOTOR_PIN_A, 0 )
            pi.softPwmWrite( self.IN_MOTOR_PIN_B, int(pwm))
        elif TYPE == DriveType.ROT_LEFT:
            pi.softPwmWrite( self.IN_MOTOR_PIN_A, int(pwm))
            pi.softPwmWrite( self.IN_MOTOR_PIN_B, 0 )

    def callback(self, gpio_pin):#mainの時だけつかう
        current_a=GPIO.input(self.IN_ENCORDER_PIN_A)
        current_b=GPIO.input(self.IN_ENCORDER_PIN_B)
    
        encoded=(current_a<<1)|current_b
        sum=(self.prev_data<<2)|encoded
    

        if (sum==0b0010 or sum==0b1011 or sum==0b1101 or sum==0b0100):
            self.angle+=self.delta
            # print ("plus", gpio_pin, self.angle)
        elif(sum==0b0001 or sum==0b0111 or sum==0b1110 or sum==0b1000):
            self.angle-=self.delta
            # print ("minus", gpio_pin, self.angle)
    
        self.prev_data=encoded


    def encorder2angle(self):   #callback使わない場合こっち使う
        current_a=GPIO.input(self.IN_ENCORDER_PIN_A)
        current_b=GPIO.input(self.IN_ENCORDER_PIN_B)
    
        encoded=(current_a<<1)|current_b
        sum=(self.prev_data<<2)|encoded
    
        if (sum==0b0010 or sum==0b1011 or sum==0b1101 or sum==0b0100):
            self.angle+=self.delta
        elif(sum==0b0001 or sum==0b0111 or sum==0b1110 or sum==0b1000):
            self.angle-=self.delta
    
        self.prev_data=encoded

    def __del__(self):
        GPIO.cleanup()
        

def main():
    try:
        #=======初期設定===================================
        #インスタンス生成
        encordered_motor_R = EncoderedMotor(Gear.MOTOR_GEAR_1, PinType.ENCORDER_1A, PinType.ENCORDER_1B, PinType.MOTOR_1A, PinType.MOTOR_1B)


        #==================================================



        while True:
            if encordered_motor_R.angle > -5:
                encordered_motor_R.motor_ctrl(DriveType.ROT_RIGHT, 10)
            elif encordered_motor_R.angle < -365:
                encordered_motor_R.motor_ctrl(DriveType.ROT_LEFT, 10)

            print(encordered_motor_R.angle)
            time.sleep(0.1)

    except KeyboardInterrupt:
        #callback登録
        GPIO.remove_event_detect(encordered_motor_R.IN_ENCORDER_PIN_A)
        GPIO.remove_event_detect(encordered_motor_R.IN_ENCORDER_PIN_B)

    del encordered_motor_R
 
if __name__ == "__main__":   
    main()