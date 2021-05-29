import RPi.GPIO as GPIO
import wiringpi as pi
import time
 
PIN_A=17
PIN_B=27
 

IN1_MOTOR_PINA = 14
IN1_MOTOR_PINB = 15
 
prev_data=0
angle=0.
delta=360./1970 #ざっとキャリブレーション済
 
 
def main():
    init()
 
    try:
        while(True):
            motor_cntl()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print ("break")
        GPIO.remove_event_detect(PIN_A)
        GPIO.remove_event_detect(PIN_B)
        GPIO.cleanup()
 
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)    

    pi.wiringPiSetupGpio()
    pi.pinMode( IN1_MOTOR_PINA, pi.OUTPUT )
    pi.pinMode( IN1_MOTOR_PINB, pi.OUTPUT )

    # モータードライバを接続したGPIOをPWM出力できるようにする
    pi.softPwmCreate( IN1_MOTOR_PINA, 0, 100 )
    pi.softPwmCreate( IN1_MOTOR_PINB, 0, 100 )  


    # モーターを停止した状態にする
    pi.softPwmWrite( IN1_MOTOR_PINA, 0 )
    pi.softPwmWrite( IN1_MOTOR_PINB, 0 )
    
    GPIO.add_event_detect(PIN_A, GPIO.BOTH, callback=callback)
    GPIO.add_event_detect(PIN_B, GPIO.BOTH, callback=callback)
 
    
def motor_cntl():
    global angle
 
    if angle>180:                               #モータ反動あり
        pi.softPwmWrite( IN1_MOTOR_PINA, 0)
        pi.softPwmWrite( IN1_MOTOR_PINB, 0 )
    elif angle<-180:
        pi.softPwmWrite( IN1_MOTOR_PINA, 0)
        pi.softPwmWrite( IN1_MOTOR_PINB, 0 )
    
def callback(gpio_pin):
    global angle, prev_data
 
    current_a=GPIO.input(PIN_A)
    current_b=GPIO.input(PIN_B)
 
    encoded=(current_a<<1)|current_b
    sum=(prev_data<<2)|encoded
 
    # print(bin(sum))
    if (sum==0b0010 or sum==0b1011 or sum==0b1101 or sum==0b0100):
        angle+=delta
        # print ("plus", gpio_pin, angle)
    elif(sum==0b0001 or sum==0b0111 or sum==0b1110 or sum==0b1000):
        angle-=delta
        # print ("minus", gpio_pin, angle)
 
    prev_data=encoded
 
if __name__ == "__main__":   
    main()