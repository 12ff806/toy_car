#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO


class Motor(object):
    def __init__(self):
        self.motor_left_ena = 2
        self.motor_right_ena = 3
        self.motor_pin = [(20, 21), (12, 13)]
        self.pwm_enable = True
        
        self.setup()

    def setup(self):
        """
        初始化 GPIO 引脚
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_left_ena, GPIO.OUT)
        GPIO.setup(self.motor_right_ena, GPIO.OUT)
        GPIO.output(self.motor_left_ena, GPIO.HIGH)
        GPIO.output(self.motor_right_ena, GPIO.HIGH)
        
        for l in self.motor_pin:
            GPIO.setup(l[0], GPIO.OUT)
            GPIO.setup(l[1], GPIO.OUT)

        self.pwm_20 = GPIO.PWM(20, 200)
        self.pwm_21 = GPIO.PWM(21, 200)
        self.pwm_12 = GPIO.PWM(12, 200)
        self.pwm_13 = GPIO.PWM(13, 200)

        self.pwm_20.start(0)
        self.pwm_21.start(0)
        self.pwm_12.start(0)
        self.pwm_13.start(0)

    def action(self, direction, l_speed=100, r_speed=100):
        """
        方向控制
        """
        if direction == "N":
            self.pwm_20.ChangeDutyCycle(r_speed)
            self.pwm_21.ChangeDutyCycle(0)
            self.pwm_12.ChangeDutyCycle(l_speed)
            self.pwm_13.ChangeDutyCycle(0)

        elif direction == "S":
            self.pwm_20.ChangeDutyCycle(0)
            self.pwm_21.ChangeDutyCycle(r_speed)
            self.pwm_12.ChangeDutyCycle(0)
            self.pwm_13.ChangeDutyCycle(l_speed)

        elif direction == "CWR":
            self.pwm_20.ChangeDutyCycle(0)
            self.pwm_21.ChangeDutyCycle(r_speed)
            self.pwm_12.ChangeDutyCycle(l_speed)
            self.pwm_13.ChangeDutyCycle(0)
            
        elif direction == "ACWR":
            self.pwm_20.ChangeDutyCycle(r_speed)
            self.pwm_21.ChangeDutyCycle(0)
            self.pwm_12.ChangeDutyCycle(0)
            self.pwm_13.ChangeDutyCycle(l_speed)

        elif direction == "STOP":
            self.pwm_20.ChangeDutyCycle(0)
            self.pwm_21.ChangeDutyCycle(0)
            self.pwm_12.ChangeDutyCycle(0)
            self.pwm_13.ChangeDutyCycle(0)


# 单独运行 可测试
if __name__ == "__main__":
    mc = Motor()

    try:
        while True:
            command = input("['N'/'S'/'CWR'/'ACWR'/'STOP'/'EXIT']: ")
            if command.upper() in ["N", "S", "CWR", "ACWR"]:
                l_speed = input("['L_SPEED']: ")
                r_speed = input("['R_SPEED']: ")
                mc.action(command.upper(), l_speed=int(l_speed), r_speed=int(r_speed))
            elif command.upper() in ["STOP"]:
                mc.action(command.upper())
            elif command.upper() in ["EXIT"]:
                GPIO.cleanup()
                break
                
    except KeyboardInterrupt as e:
        GPIO.cleanup()


