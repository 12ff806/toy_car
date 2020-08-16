#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "12ff806"
__date__ = "10/16/2018"
__description__ = "PID"


class FeedbackControl(object):
    """
    PID
    """
    def __init__(self, target_value, kp, ki=None, kd=None):
        self.target_value = target_value
        self.kp = kp
        if not ki:
            self.ki = 0
        else:
            self.ki = ki
        if not kd:
            self.kd = 0
        else:
            self.kd = kd
        self.error = 0
        self.previous_error = 0
        self.sum_error = 0
    
    def p_control(self, current_value):
        """
        P
        """
        # 比例
        self.error = self.target_value - current_value
        p = self.error * self.kp

        return p

    def pd_control(self, current_value):
        """
        PD
        """
        # 比例
        self.error = self.target_value - current_value
        p = self.error * self.kp

        # 微分
        d = (self.error - self.previous_error) * self.kd
        self.previous_error = self.error

        pd = p + d
        return pd

    def pid_control(self, current_value):
        """
        PID
        """
        # 比例
        self.error = self.target_value - current_value
        p = self.error * self.kp

        # 微分
        d = (self.error - self.previous_error) * self.kd
        self.previous_error = self.error

        # 积分
        i = self.sum_error * self.ki
        self.sum_error += self.error

        pid = p + d + i
        return pid
        

if __name__ == "__main__":
    fbc = FeedbackControl(90, 0.2, ki=0.05, kd=0.1)
    print(fbc.pid_control(95))
        
