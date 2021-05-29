import RPi.GPIO as GPIO
import wiringpi as pi
import time
 
ENCORDER_PIN_1A = 17
ENCORDER_PIN_1B = 27
 
MOTOR_PIN_1A = 14
MOTOR_PIN_1B = 15

MOTOR_GEAR = 1970   #ざっとキャリブレーション

 
class EncoderedMotor():
    angle = 0 
    prev_data = 0

    # def __init__(self):

    def setDelta(self, gears):
        self.delta = 360./gears

    def setEncorderPin(self, ENCORDER_PIN_A, ENCORDER_PIN_B):
        self.IN_ENCORDER_PIN_A = ENCORDER_PIN_A
        self.IN_ENCORDER_PIN_B = ENCORDER_PIN_B

    def setMotorPin(self, MOTOR_PIN_A, MOTOR_PIN_B):
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
        pi.softPwmWrite( self.IN_MOTOR_PIN_A, 10 )
        pi.softPwmWrite( self.IN_MOTOR_PIN_B, 0 )
        
        GPIO.add_event_detect(self.IN_ENCORDER_PIN_A, GPIO.BOTH, callback=self.callback)
        GPIO.add_event_detect(self.IN_ENCORDER_PIN_B, GPIO.BOTH, callback=self.callback)

    def motor_ctrl(self):
        if self.angle>180:                               #モータ反動あり
            pi.softPwmWrite( self.IN_MOTOR_PIN_A, 0 )
            pi.softPwmWrite( self.IN_MOTOR_PIN_B, 10 )
        elif self.angle<-180:
            pi.softPwmWrite( self.IN_MOTOR_PIN_A, 10 )
            pi.softPwmWrite( self.IN_MOTOR_PIN_B, 0 )


    def callback(self, gpio_pin):
 
        current_a=GPIO.input(self.IN_ENCORDER_PIN_A)
        current_b=GPIO.input(self.IN_ENCORDER_PIN_B)
    
        encoded=(current_a<<1)|current_b
        sum=(self.prev_data<<2)|encoded
    
        # print(bin(sum))
        if (sum==0b0010 or sum==0b1011 or sum==0b1101 or sum==0b0100):
            self.angle+=self.delta
            # print ("plus", gpio_pin, angle)
        elif(sum==0b0001 or sum==0b0111 or sum==0b1110 or sum==0b1000):
            self.angle-=self.delta
            # print ("minus", gpio_pin, angle)
    
        self.prev_data=encoded



def main():
    #=======初期設定(本当は1行で済ませたい)===================================
    encordered_motor_R = EncoderedMotor()#インスタンス生成
    encordered_motor_R.setDelta(MOTOR_GEAR) #モーター歯数代入
    encordered_motor_R.setEncorderPin(ENCORDER_PIN_1A, ENCORDER_PIN_1B) #エンコーダーピン指定
    encordered_motor_R.setMotorPin(MOTOR_PIN_1A, MOTOR_PIN_1B) #モーターピン指定
    encordered_motor_R.setup() #モーターとエンコーダーのセットアップ
    #=========================================================================

    try:
        while(True):
            encordered_motor_R.motor_ctrl()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print ("while_break")
        GPIO.remove_event_detect(encordered_motor_R.IN_ENCORDER_PIN_A)
        GPIO.remove_event_detect(encordered_motor_R.IN_ENCORDER_PIN_B)
        GPIO.cleanup()
 
if __name__ == "__main__":   
    main()