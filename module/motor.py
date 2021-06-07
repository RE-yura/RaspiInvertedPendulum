# ライブラリのインポート
import RPi.GPIO as GPIO
import wiringpi as pi
import time


# モータードライバーを接続したGPIOピンの定義
IN1_MOTOR_PINA = 14
IN1_MOTOR_PINB = 15
# 各種設定
pi.wiringPiSetupGpio()
pi.pinMode(IN1_MOTOR_PINA, pi.OUTPUT)
pi.pinMode(IN1_MOTOR_PINB, pi.OUTPUT)

# モータードライバを接続したGPIOをPWM出力できるようにする
pi.softPwmCreate(IN1_MOTOR_PINA, 0, 100)
pi.softPwmCreate(IN1_MOTOR_PINB, 0, 100)

# モーターを停止した状態にする
pi.softPwmWrite(IN1_MOTOR_PINA, 0)
pi.softPwmWrite(IN1_MOTOR_PINB, 0)

# ボタンが押された回数を初期化
countPower = 0

# 正常処理
try:
    while True:
        if(time.time() % 4 < 2):
            pi.softPwmWrite(IN1_MOTOR_PINA, 10)
            pi.softPwmWrite(IN1_MOTOR_PINB, 0)
        else:
            pi.softPwmWrite(IN1_MOTOR_PINA, 0)
            pi.softPwmWrite(IN1_MOTOR_PINB, 10)

# プログラム強制終了時にモーターを止める
except KeyboardInterrupt:
    pi.softPwmWrite(IN1_MOTOR_PINA, 0)
    pi.softPwmWrite(IN1_MOTOR_PINB, 0)
