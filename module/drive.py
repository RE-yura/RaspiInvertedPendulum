import time
import enum as Enum
from Encorder import *
from gyro import *


class Motor(Enum):
    RIGHT = 0
    LEFT = 1


class DriveUnit():

    def __init__(self, glist):
        self.ACT_FORWARD = 0
        self.ACT_BACKWARD = 1
        self.ACT_BREAK = 2
        self.ACT_STOP = 3

        self.last_err = 0

        self.U_MAX = 100

        self.err_p = 0
        self.err_d = 0
        self.err_i = 0
        self.gain_p = 0
        self.gain_d = 0
        self.gain_i = 0
        self.exu = 0
        self.u = 0

        self.ANG_VELO = 780  # 角速度±780dps
        self.dt = 0
        self.now = 0
        self.pre_time = time.time()

        # インスタンス生成
        self.gyro = Gyro()
        self.motor_r = EncoderedMotor(Gear.MOTOR_GEAR_1, PinType.ENCORDER_1A,
                                     PinType.ENCORDER_1B, PinType.MOTOR_1A, PinType.MOTOR_1B)
        self.motor_l = EncoderedMotor(Gear.MOTOR_GEAR_2, PinType.ENCORDER_2A,
                                     PinType.ENCORDER_2B, PinType.MOTOR_2A, PinType.MOTOR_2B)

        # ゲイン登録
        self.set_gain(glist)

    def drive(self, dir, pwm):
        # 車体移動
        if dir == self.ACT_FORWARD:
            self.motor_r.motor_ctrl(DriveType.ROT_RIGHT, abs(pwm))
            self.motor_l.motor_ctrl(DriveType.ROT_LEFT, abs(pwm))
        elif dir == self.ACT_BACKWARD:
            self.motor_r.motor_ctrl(DriveType.ROT_LEFT, abs(pwm))
            self.motor_l.motor_ctrl(DriveType.ROT_RIGHT, abs(pwm))

    def calc_dt(self):
        self.now = time.time()
        self.dt = (self.now - self.pre_time)
        self.pre_time = self.now

    def calc_errp(self):
        self.err_p = (self.gyro.angle / 90.0 - 1) * self.U_MAX  # P成分：傾き-180～0度 → -100～100

        if abs(self.err_p) < 0.01:
            self.err_p = 0

    def calc_errd(self):
        self.err_d = (self.err_p - self.last_err) / self.dt / self.ANG_VELO * self.U_MAX  # D成分：角速度±780dps → -100～100
        if abs(self.err_d) < 1:
            self.err_d = 0
        self.last_err = self.err_p

    def calc_erri(self):
        self.err_i += self.err_p * self.dt  # I成分

    def position_control(self):
        self.gyro.get_accel()
        self.gyro.get_gyro()
        self.gyro.get_angle()

        # dt計算
        self.calc_dt()

        # 偏差計算
        self.calc_errp()
        self.calc_errd()
        self.calc_erri()

        # PWM計算
        self.u = self.exu * self.u + (1 - self.exu) * (self.gain_p * self.err_p +
                                                       self.gain_d * self.err_d + self.gain_i * self.err_i)

        if self.u > 100:
            self.u = 100
        elif self.u < -100:
            self.u = -100

        # モーター駆動
        self.balance()

    def set_gain(self, glist):
        self.gain_p = glist[0]
        self.gain_d = glist[1]
        self.gain_i = glist[2]

    def balance(self):
        if self.u > 0:
            self.drive(self.ACT_FORWARD, self.u)
        else:
            self.drive(self.ACT_BACKWARD, self.u)

    def __del__(self):
        del self.gyro
        del self.motor_r
        del self.motor_l


def main():
    try:
        # =======初期設定===================================
        unit = DriveUnit([10, 0, 0])
        gyro = Gyro()
        # unit = DriveUnit(0, 1200, 0)
        # ==================================================

        while True:
            # unit.drive(unit.ACT_BACKWARD, 10)
            unit.position_control()
            print('{0:4.2f}' .format(unit.gyro.angle))
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    del unit


if __name__ == "__main__":
    main()
