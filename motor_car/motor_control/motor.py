#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import threading
import time


class MotorCar(object):
    def __init__(self):
        self.motor_ena = 2
        self.logic = [(20, 21), (12, 13)]
        self.TRIG = 17
        self.ECHO = 18
        self.L_TRIG = 23
        self.L_ECHO = 24
        self.R_TRIG = 16
        self.R_ECHO = 19
        self.p_status = None
        self.status = None
        
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_ena, GPIO.OUT)
        GPIO.output(self.motor_ena, GPIO.HIGH)

        for l in self.logic:
            GPIO.setup(l[0], GPIO.OUT)
            GPIO.setup(l[1], GPIO.OUT)

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setup(self.L_TRIG, GPIO.OUT)
        GPIO.setup(self.L_ECHO, GPIO.IN)
        GPIO.setup(self.R_TRIG, GPIO.OUT)
        GPIO.setup(self.R_ECHO, GPIO.IN)

    def distance(self, trig, echo):
        GPIO.output(trig, 0)
        time.sleep(0.000002)
        GPIO.output(trig, 1)
        time.sleep(0.00001)
        GPIO.output(trig, 0)

        while GPIO.input(echo) == 0:
            a = 0
        time1 = time.time()
        while GPIO.input(echo) == 1:
            a = 1
        time2 = time.time()

        during = time2 - time1
        return ((during * 340) / 2) * 100

    def get_dis_loop(self, t_p_status=None):
        while True:
            dis = self.distance(self.TRIG, self.ECHO)
            if t_p_status == "AUTO":
                break
            if self.status == "MO":
                break

            if dis < 30:
                if self.status == "MO":
                    break
                self.action("S")
                if self.status == "MO":
                    break
                time.sleep(1.5)
                if self.status == "MO":
                    break
                l_dis = self.distance(self.L_TRIG, self.L_ECHO)
                if self.status == "MO":
                    break
                r_dis = self.distance(self.R_TRIG, self.R_ECHO)
                if self.status == "MO":
                    break
                if l_dis > r_dis:
                    self.action("W")
                else:
                    self.action("E")
                if self.status == "MO":
                    break
                self.action("N")
                break

            time.sleep(0.1)

    def action(self, direction, t_p_status=None):
        self.setup()
        
        if direction == "N":
            for l in self.logic:
                GPIO.output(l[0], GPIO.HIGH)
                GPIO.output(l[1], GPIO.LOW)
            if self.status == "AUTO":
                t = threading.Thread(target=self.get_dis_loop, args=(t_p_status, ))
                t.start()
        elif direction == "S":
            for l in self.logic:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.HIGH)
        elif direction == "W":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            time.sleep(1.5)
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
        elif direction == "E":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
            time.sleep(1.5)
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
        elif direction == "P":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)


if __name__ == "__main__":
    mc = MotorCar()
    while True:
        try:
            command = input("['E(AUTO)']/['W'-'S'-'A'-'D'-'Q']/['Z']: ")
            if command.upper() == "E":
                t_p_status = mc.status
                mc.status = "AUTO"
                mc.action("N", t_p_status)
            elif command.upper() in ["W", "S", "A", "D", "Q"]:
                mc.p_status = mc.status
                mc.status = "MO"
                km = {"W": "N", "S": "S", "A": "W", "D": "E", "Q": "P"}
                mc.action(km[command.upper()])
            elif command.upper() == "Z":
                break
            else:
                print("Invalid Command")
        except KeyboardInterrupt:
            break
                
    GPIO.cleanup()
