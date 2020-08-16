#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import threading
import time
import serial


class MotorCar(object):
    def __init__(self):
        # 左侧电机使能引脚
        self._motor_left_ena = 2
        
        # 右侧电机使能引脚
        self._motor_right_ena = 3
        
        # 左右侧电机控制引脚
        self.motor_pin = [(20, 21), (12, 13)]
        
        # PWM使能
        self._pwm_enable = True
        
        # 右侧脉冲初始值
        self._pwm_right_dc = 50

        # 右侧脉冲临时值
        self._pwm_right_dc_temp = 50
        
        # 左侧脉冲初始值
        self._pwm_left_dc = 50
        
        # 初始化串口
        self.ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=None)
        
        # 保存偏航角
        self.yaw = None

        # 目标航向角度
        self.target_yaw = None

        # 比例控制参数
        self.kp = 0.01

        # 积分控制参数
        self.ki = 0.000005
        
        # 微分控制参数
        self.kd = 0.005

        # 当前误差
        self.error = 0

        # 上次误差
        self.previous_error = 0

        # 所有次数误差和
        self.sum_error = 0
        
        # 小车当前状态
        self.status = "STOP"
        
        # 是否为初始时刻
        self.firsttime = False

        self.setup()

    def setup(self):
        """
        初始化 GPIO 引脚
        """
        # 引脚定义模式
        GPIO.setmode(GPIO.BCM)

        # 设置motor enable引脚
        GPIO.setup(self._motor_left_ena, GPIO.OUT)
        GPIO.setup(self._motor_right_ena, GPIO.OUT)
        #GPIO.output(self.motor_ena, GPIO.HIGH)

        # 设置motor control引脚
        for l in self.motor_pin:
            GPIO.setup(l[0], GPIO.OUT)
            GPIO.setup(l[1], GPIO.OUT)

    def get_current_yaw(self):
        """
        获取当前的偏航角
        """
        while True:
            try:
                data = self.ser.read()
                time.sleep(0.08)
                remaining_bytes = self.ser.inWaiting()
                data += self.ser.read(remaining_bytes)
                data = list(data)
                if len(data) != 44:
                    time.sleep(0.01)
                    continue
                self.yaw = ((data[29]<<8)|data[26])/32768*180
            except Exception as e:
                print("Exception:", e)

    def adjustment(self):
        """
        PID控制
        """
        # 暂停1s等待姿态传感器稳定
        time.sleep(1)
        
        while True:
            # 向前直走
            if self.status in ["N", "S"]:
                if self.firsttime == True:
                    # 设置目标航向角
                    while True:
                        if self.yaw:
                            self.target_yaw = self.yaw
                            self.firsttime = False
                            break
                        else:
                            pass
            
                # 进行PID控制
                while True:
                    if self.yaw:
                        current_yaw = self.yaw
                        break
                    else:
                        pass
                        
                error = self.target_yaw - current_yaw
                if self.target_yaw >= 0 and self.target_yaw < 45:
                    # 右偏
                    if error < 0 and abs(error) >= 270:
                        error = error + 360
                        
                elif self.target_yaw > 315 and self.target_yaw <= 360:
                    # 左偏
                    if error > 0 and error >= 270:
                        error = error - 360
                        
                # 比例控制
                p = error * self.kp

                # 微分控制
                d = (error - self.previous_error) * self.kd
                self.previous_error = error

                # 积分控制
                i = self.sum_error * self.ki
                self.sum_error += error

                pid = p + i + d
                pd = p + d
                print("self._pwm_right_dc: ", self._pwm_right_dc)
                if (self._pwm_right_dc_temp + pid) <= 100.0 and (self._pwm_right_dc_temp + pid) >= 0.0:
                    self._pwm_right_dc_temp += pid
                    self._pwm_right_dc = float("{:.1f}".format(self._pwm_right_dc_temp))
                    #self._pwm_right_dc += pd
                elif (self._pwm_right_dc_temp + pid) > 100.0:
                    self._pwm_right_dc = 100.0
                elif (self._pwm_right_dc_temp + pid) < 0.0:
                    self._pwm_right_dc = 0.0
                print("pd: ", pid)
                print("self._pwm_right_dc: ", self._pwm_right_dc)
                print("self._pwm_left_dc: ", self._pwm_left_dc)

            # 停止
            elif self.status in ["STOP"]:
                self.previous_error = 0
                self.sum_error = 0

            # 顺时针旋转
            elif self.status in ["CWR"]:
                self.previous_error = 0
                self.sum_error = 0

                # 将PWM还原
                self._pwm_right_dc = 100
                self._pwm_left_dc = 100
                
                print("right_dc: ", self._pwm_right_dc)
                print("left_dc: ", self._pwm_left_dc)

                # 获取当前航向角
                while True:
                    if self.yaw:
                        self.current_yaw = self.yaw
                        print("self.current_yaw: ", self.current_yaw)
                        break
                    else:
                        pass

                # 顺时针转90度
                if self.current_yaw > 90:
                    self.target_yaw = self.current_yaw - 90
                    while self.yaw > self.target_yaw:
                        print("self.yaw: ", self.yaw)
                        pass
                    self.action("STOP")
                    print("STOP")
                    print("self.yaw: ", self.yaw)
                    print("self.target_yaw: ", self.target_yaw)
                    
                elif self.current_yaw < 90:
                    self.target_yaw = 360 + self.current_yaw - 90
                    while self.yaw > 0 and self.yaw < self.current_yaw + 60:
                    #while self.yaw > 0:
                        print("self.yaw: ", self.yaw)
                        pass
                    while self.yaw > self.target_yaw:
                        print("self.yaw: ", self.yaw)
                        pass
                    self.action("STOP")
                    print("STOP")
                    print("self.yaw: ", self.yaw)
                    print("self.target_yaw: ", self.target_yaw)
            
            # 逆时针旋转
            elif self.status in ["ACWR"]:
                self.previous_error = 0
                self.sum_error = 0

                # 将PWM还原
                self._pwm_right_dc = 100
                self._pwm_left_dc = 100
                
                print("right_dc: ", self._pwm_right_dc)
                print("left_dc: ", self._pwm_left_dc)
                
                # 获取当前航向角
                self.current_yaw = self.yaw
                print("self.current_yaw: ", self.current_yaw)

                # 逆时针转90度
                if self.current_yaw < 270:
                    self.target_yaw = self.current_yaw + 90
                    while self.yaw < self.target_yaw:
                        print("self.yaw: ", self.yaw)
                        pass
                    self.action("STOP")
                    print("STOP")
                    print("self.yaw: ", self.yaw)
                    print("self.target_yaw: ", self.target_yaw)
                    
                elif self.current_yaw > 270:
                    self.target_yaw = self.current_yaw + 90 - 360
                    while self.yaw > (self.current_yaw - 60) and self.yaw < 360:
                    #while self.yaw < 360:
                        print("self.yaw: ", self.yaw)
                        pass
                    while self.yaw < self.target_yaw:
                        print("self.yaw: ", self.yaw)
                        pass
                    self.action("STOP")
                    print("STOP")
                    print("self.yaw: ", self.yaw)
                    print("self.target_yaw: ", self.target_yaw)

    def pwm_control(self):
        """
        PWM 调速
        """
        pl = GPIO.PWM(self._motor_left_ena, 200)
        pr = GPIO.PWM(self._motor_right_ena, 200)
        pl.start(self._pwm_left_dc)
        pr.start(self._pwm_right_dc)
        while True:
            try:
                if self._pwm_enable:
                    #pl.start(self._pwm_left_dc)
                    #pr.start(self._pwm_right_dc)
                    #time.sleep(0.1)
                    pr.ChangeDutyCycle(self._pwm_right_dc)
                    pr.ChangeDutyCycle(self._pwm_left_dc)
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
        # 往前走
        if direction == "N":
            for l in self.motor_pin:
                GPIO.output(l[0], GPIO.HIGH)
                GPIO.output(l[1], GPIO.LOW)
            self.status = "N"
            self.firsttime = True

        # 往后走
        elif direction == "S":
            for l in self.motor_pin:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.HIGH)
            self.status = "S"
            self.firsttime = True

        # 顺时针转
        elif direction == "CWR":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            self.status = "CWR"

        # 逆时针转
        elif direction == "ACWR":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            self.status = "ACWR"

        # 停止
        elif direction == "STOP":
            for l in self.motor_pin:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.LOW)
            self.status = "STOP"


if __name__ == "__main__":
    mc = MotorCar()

    # 开启 PWM 调速线程
    thread_pwm = threading.Thread(target=mc.pwm_control)
    thread_pwm.start()

    # 开启获取航向角线程
    thread_yaw = threading.Thread(target=mc.get_current_yaw)
    thread_yaw.start()

    # 开启PID控制线程
    thread_pid = threading.Thread(target=mc.adjustment)
    thread_pid.start()

    # 等待接收指令
    while True:
        try:
            command = input("['N'/'S'/'CWR'/'ACWR'/'STOP']: ")
            if command.upper() in ["N", "S", "CWR", "ACWR", "STOP"]:
                mc.action(command.upper())
            else:
                print("Invalid Command")
        except KeyboardInterrupt:
            break
            
    GPIO.cleanup()
    exit(0)
