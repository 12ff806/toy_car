#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import time


class Motor(object):
    def __init__(self):
        self.motor_ena = 2
        self.logic = [(20, 21), (12, 13), (22, 25), (26, 27)]
        self.current_status = None
        self.p_enable = None

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_ena, GPIO.OUT)
        #GPIO.output(self.motor_ena, GPIO.HIGH)
        
        for l in self.logic:
            GPIO.setup(l[0], GPIO.OUT)
            GPIO.setup(l[1], GPIO.OUT)
    
    def pwm_action(self, direction):
        self.setup()

        status = None
        if direction == "N":
            status = "N"
            for l in self.logic:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.HIGH)

        elif direction == "CWR":
            status = "CWR"
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)

        elif direction == "ACWR":
            status = "ACWR"
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.HIGH)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)

        elif direction == "STOP":
            status = "STOP"
            for l in self.logic:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.LOW)
        
        self.p_enable = GPIO.PWM(self.motor_ena, 100)
        while True:
            #if self.current_status == status:
            #    self.p_enable.start(70)
            #else:
            #    break
            
            self.p_enable.start(70)

    def stop(self):
        try:
            self.p_enable.stop()
        except:
            pass

        GPIO.cleanup()


if __name__ == "__main__":
    m = Motor()
    m.pwm_action("CWR")
        
