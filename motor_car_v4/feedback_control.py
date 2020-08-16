#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class FeedbackControl(object):
    """
    PID 控制
    """
    def __init__(self, kp=0.1, ki=0.000005, kd=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    @staticmethod
    def calculate_error(target_value, value):
        """
        计算误差
        """
        error = target_value - value
        
        if target_value >= 0 and target_value < 45:
            # 右偏
            if error < 0 and abs(error) >= 270:
                error = error + 360
        elif target_value > 315 and target_value <= 360:
            # 左偏
            if error > 0 and error >= 270:
                error = error - 360

        return error
    
    def p_control(self, target_value, value):
        """
        比例控制
        """
        error = self.calculate_error(target_value, value)
        p = error * self.kp
        self.integral += error
        return p

    def pd_control(self, target_value, value):
        """
        比例/微分控制
        """
        p = self.p_control(target_value, value)
        error = self.calculate_error(target_value, value)
        d = (error - self.previous_error) * self.kd
        self.previous_error = error
        pd = p + d
        return pd

    def pid_control(self, target_value, value):
        """
        比例/积分/微分控制
        """
        pd = self.pd_control(target_value, value)
        i = self.integral * self.ki
        pid = pd + i
        return pid
        
