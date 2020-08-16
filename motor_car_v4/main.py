#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import RPi.GPIO as GPIO
from motor_driver import Motor
from motion_sensor import Motion
from feedback_control import FeedbackControl


class Car(object):
    """
    综合控制类
    """
    def __init__(self):
        # 姿态传感器实例
        self.motion = Motion()

        # 马达控制实例
        self.motor = Motor()

        # 小车当前状态
        self.status = "STOP"

        # 最大PWM脉宽
        self.MAX_PWM_VALUE = 100.0

        # 做小PWM脉宽
        self.MIN_PWM_VALUE = 0.0

        # 左侧车轮默认PWM脉宽
        self.left_pwm_value = 50
        
        # 右侧车轮默认PWM脉宽
        self.right_pwm_value = 50

        # 右侧车轮临时PWM脉宽
        self.right_pwm_temp_value = 50
        
        # 上次误差
        #self.previous_error = 0

        # 所有次数误差和
        #self.integral = 0

    def run(self, direction):
        """
        行走过程控制
        """
        # 向前走直线
        if direction == "N":
            # PID控制实例
            fbc = FeedbackControl()

            # 获取当前航向角度作为目标角度
            target_yaw = self.motion.get_yaw()

            # 变更小车状态
            self.status = "N"

            # 驱动马达向前走
            self.motor.action("N", self.left_pwm_value, self.right_pwm_value)

            # pid控制
            while True:
                # 获取当前航向角
                current_yaw = self.motion.get_yaw()

                # 通过PID计算调整值
                pid = fbc.pid_control(target_yaw, current_yaw)

                if (self.right_pwm_temp_value + pid) <= self.MAX_PWM_VALUE and (self.right_pwm_temp_value + pid) >= self.MIN_PWM_VALUE:
                    self.right_pwm_temp_value += pid
                    self.right_pwm_value = float("{:.1f}".format(self.right_pwm_temp_value))
                elif (self.right_pwm_temp_value + pid) > self.MAX_PWM_VALUE:
                    self.right_pwm_value = self.MAX_PWM_VALUE
                elif (self.right_pwm_temp_value + pid) < self.MIN_PWM_VALUE:
                    self.right_pwm_value = self.MIN_PWM_VALUE

                # 重新驱动马达
                self.motor.action("N", self.left_pwm_value, self.right_pwm_value)

                print("target: {}, current: {}, left_pwm: {}, right_pwm: {}".format(target_yaw, current_yaw, self.left_pwm_value, self.right_pwm_value))

        # 顺时针转90度
        elif direction == "CWR":
            
            # 获取当前航向角度计算出目标角度
            start_yaw = self.motion.get_yaw()

            # 顺时针转弯
            self.motor.action("CWR", 50, 50)
            
            if start_yaw > 90:
                target_yaw = start_yaw - 90
                while True:
                    # 获取当前航向角
                    current_yaw = self.motion.get_yaw()
                    if current_yaw <= target_yaw:
                        break
                # 停止
                self.motor.action("STOP")
                print("start: {}, target: {}, current: {}".format(start_yaw, target_yaw, current_yaw))

            elif start_yaw < 90:
                target_yaw = start_yaw - 90 + 360
                
                while True:
                    # 获取当前航向角
                    current_yaw = self.motion.get_yaw()
                    if current_yaw > 0 and current_yaw < start_yaw + 60:
                        continue
                    if current_yaw <= target_yaw:
                        break
                
                # 停止
                self.motor.action("STOP")
                print("start: {}, target: {}, current: {}".format(start_yaw, target_yaw, current_yaw))
                

if __name__ == "__main__":
    car = Car()
    car.run("N")

