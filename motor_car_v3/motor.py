#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import threading
import time


class MotorCar(object):
    def __init__(self):
        self.motor_ena = 2
        self.motor_pin = [(20, 21), (12, 13)]
        self.ra_pin = 22
        self.rb_pin = 25
        self.la_pin = 26
        self.lb_pin = 27
        self._pwm_enable = True
        self._pwm_value = 100
        self.direction = None
        self.speed = None
        self.outcome = [0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0]
        self.last_r_ab = 0b00
        self.last_l_ab = 0b00
        self.r_counter = 0
        self.l_counter = 0
        
        self.setup()

    def setup(self):
        """
        初始化 GPIO 引脚
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_ena, GPIO.OUT)
        #GPIO.output(self.motor_ena, GPIO.HIGH)

        for l in self.motor_pin:
            GPIO.setup(l[0], GPIO.OUT)
            GPIO.setup(l[1], GPIO.OUT)

        GPIO.setup(self.la_pin, GPIO.IN)
        GPIO.setup(self.lb_pin, GPIO.IN)
        GPIO.setup(self.ra_pin, GPIO.IN)
        GPIO.setup(self.rb_pin, GPIO.IN)

    def _right_hall(self):
        """
        右侧电机的霍尔测速
        """
        while True:
            try:
                A = GPIO.input(self.ra_pin)
                B = GPIO.input(self.rb_pin)

                current_AB = (A << 1) | B
                position = (self.last_r_ab << 2) | current_AB

                self.r_counter += self.outcome[position]
                self.last_r_ab = current_AB
            except:
                pass

    def _left_hall(self):
        """
        左侧电机的霍尔测速
        """
        while True:
            try:
                A = GPIO.input(self.la_pin)
                B = GPIO.input(self.lb_pin)

                current_AB = (A << 1) | B
                position = (self.last_l_ab << 2) | current_AB

                self.l_counter += self.outcome[position]
                self.last_l_ab = current_AB
            except:
                pass

    def get_current_status(self):
        """
        获取当前状态 速度和方向
        """
        # 左右两侧电机速度
        time1 = time.time()
        r_counter1 = self.r_counter
        l_counter1 = self.l_counter
        time.sleep(2)
        time2 = time.time()
        r_counter2 = self.r_counter
        l_counter2 = self.l_counter
        
        print(time2 - time1)
        print(r_counter2 - r_counter1)
        print(l_counter2 - l_counter1)
        print(r_counter2)
        print(r_counter1)
        print(l_counter2)
        print(l_counter1)

        r_speed = (r_counter2 - r_counter1) / (time2 - time1)
        l_speed = (l_counter2 - l_counter1) / (time2 - time1)

        # 右侧电机方向
        r_direction = None
        if r_counter2 - r_counter1 > 0:
            r_direction = "N"
        elif r_counter2 - r_counter1 < 0:
            r_direction = "S"
        else:
            r_direction = "STOP"

        # 左侧电机方向
        l_direction = None
        if l_counter2 - l_counter1 > 0:
            l_direction = "S"
        elif l_counter2 - l_counter1 < 0:
            l_direction = "N"
        else:
            l_direction = "STOP"
        
        return (r_direction, r_speed, l_direction, l_speed)
        
    def set_pwm_value(self, value=50):
        """
        设置 PWM 空占比
        """
        self._pwm_value = value

    def pwm_control(self):
        """
        PWM 调速
        """
        p = GPIO.PWM(self.motor_ena, 200)
        while True:
            try:
                if self._pwm_enable:
                    p.start(self._pwm_value)
                else:
                    try:
                        p.stop()
                    except:
                        pass
            except:
                pass

    def action(self, direction):
        """
        方向控制
        """
        if direction == "N":
            for l in self.motor_pin:
                GPIO.output(l[0], GPIO.HIGH)
                GPIO.output(l[1], GPIO.LOW)

        elif direction == "S":
            for l in self.motor_pin:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.HIGH)
        elif direction == "CWR":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
        elif direction == "ACWR":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
        elif direction == "TNR":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
        elif direction == "TNL":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
        elif direction == "TSR":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
        elif direction == "TSL":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
        elif direction == "STOP":
            for l in self.motor_pin:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.LOW)


if __name__ == "__main__":
    mc = MotorCar()

    # 开启 PWM 调速线程
    thread_pwm = threading.Thread(target=mc.pwm_control)
    thread_pwm.start()

    # 开启右侧霍尔测速脉冲计算线程
    thread_r_hall = threading.Thread(target=mc._right_hall)
    thread_r_hall.start()
    
    # 开启左侧霍尔测速脉冲计算线程
    thread_l_hall = threading.Thread(target=mc._left_hall)
    thread_l_hall.start()

    # 等待接收指令
    while True:
        try:
            command = input("['STATUS'/'SPEED'/'N'/'S'/'CWR'/'ACWR'/'TNR'/'TNL'/'TSR'/'TSL'/'STOP'/'EXIT']: ")
            if command.upper() in ["N", "S", "CWR", "ACWR", "TNR", "TNL", "TSR", "TSL", "STOP"]:
                mc.action(command.upper())
            elif command.upper() == "STATUS":
                r_direction, r_speed, l_direction, l_speed = mc.get_current_status()
                print("right direction: {}, right speed: {:0.1f}, left direction: {}, left speed: {:0.1f}".format(r_direction, r_speed, l_direction, l_speed))
            elif command.upper() == "SPEED":
                value = input("Value of Speed[20-100]: ")
                value = int(value)
                if value >= 20 and value <=100:
                    mc.set_pwm_value(value)
                else:
                    print("Invalid Value")
            elif command.upper() == "EXIT":
                break
            else:
                print("Invalid Command")
        except KeyboardInterrupt:
            break
            
    GPIO.cleanup()
    exit(0)
