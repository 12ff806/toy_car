#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import threading
import time


class MotorCar(object):
    def __init__(self):
        self.motor_ena = 2
        self.logic = [(20, 21), (12, 13), (22, 25), (26, 27)]
        self.TRIG = 17
        self.ECHO = 18
        self.L_TRIG = 23
        self.L_ECHO = 24
        self.R_TRIG = 16
        self.R_ECHO = 19
        self.B_TRIG = 5
        self.B_ECHO = 6

        self.p_status = "MO"
        self.status = "MO"
        self.direction = "STOP"
        
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
        GPIO.setup(self.B_TRIG, GPIO.OUT)
        GPIO.setup(self.B_ECHO, GPIO.IN)

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

    def get_dis_loop(self):
        while True:
            if self.status == "MO":
                break
            if self.direction == "N":
                if self.status == "MO":
                    break
                n_dis = self.distance(self.TRIG, self.ECHO)
                if self.status == "MO":
                    break
                if n_dis < 30:
                    if self.status == "MO":
                        break
                    s_dis = self.distance(self.B_TRIG, self.B_ECHO)
                    if self.status == "MO":
                        break
                    w_dis = self.distance(self.L_TRIG, self.L_ECHO)
                    if self.status == "MO":
                        break
                    e_dis = self.distance(self.R_TRIG, self.R_ECHO)
                    if self.status == "MO":
                        break
                    if s_dis > w_dis and s_dis > e_dis:
                        if self.status == "MO":
                            break
                        self.action("S")
                        self.direction = "S"
                        if self.status == "MO":
                            break
                    elif w_dis > s_dis and w_dis > e_dis:
                        if self.status == "MO":
                            break
                        self.action("W")
                        self.direction = "W"
                        if self.status == "MO":
                            break
                    elif e_dis > s_dis and e_dis > w_dis:
                        if self.status == "MO":
                            break
                        self.action("E")
                        self.direction = "E"
                        if self.status == "MO":
                            break
            if self.status == "MO":
                break
            elif self.direction =="S":
                if self.status == "MO":
                    break
                s_dis = self.distance(self.B_TRIG, self.B_ECHO)
                if self.status == "MO":
                    break
                if s_dis < 30:
                    if self.status == "MO":
                        break
                    n_dis = self.distance(self.TRIG, self.ECHO)
                    if self.status == "MO":
                        break
                    w_dis = self.distance(self.L_TRIG, self.L_ECHO)
                    if self.status == "MO":
                        break
                    e_dis = self.distance(self.R_TRIG, self.R_ECHO)
                    if self.status == "MO":
                        break
                    if n_dis > w_dis and n_dis > e_dis:
                        if self.status == "MO":
                            break
                        self.action("N")
                        self.direction = "N"
                        if self.status == "MO":
                            break
                    elif w_dis > n_dis and w_dis > e_dis:
                        if self.status == "MO":
                            break
                        self.action("W")
                        self.direction = "W"
                        if self.status == "MO":
                            break
                    elif e_dis > n_dis and e_dis > w_dis:
                        if self.status == "MO":
                            break
                        self.action("E")
                        self.direction = "E"
                        if self.status == "MO":
                            break
            if self.status == "MO":
                break
            elif self.direction =="W":
                if self.status == "MO":
                    break
                w_dis = self.distance(self.L_TRIG, self.L_ECHO)
                if self.status == "MO":
                    break
                if w_dis < 30:
                    if self.status == "MO":
                        break
                    n_dis = self.distance(self.TRIG, self.ECHO)
                    if self.status == "MO":
                        break
                    s_dis = self.distance(self.B_TRIG, self.B_ECHO)
                    if self.status == "MO":
                        break
                    e_dis = self.distance(self.R_TRIG, self.R_ECHO)
                    if self.status == "MO":
                        break
                    if n_dis > s_dis and n_dis > e_dis:
                        if self.status == "MO":
                            break
                        self.action("N")
                        self.direction = "N"
                        if self.status == "MO":
                            break
                    elif s_dis > n_dis and s_dis > e_dis:
                        if self.status == "MO":
                            break
                        self.action("S")
                        self.direction = "S"
                        if self.status == "MO":
                            break
                    elif e_dis > n_dis and e_dis > s_dis:
                        if self.status == "MO":
                            break
                        self.action("E")
                        self.direction = "E"
                        if self.status == "MO":
                            break
            if self.status == "MO":
                break
            elif self.direction =="E":
                if self.status == "MO":
                    break
                e_dis = self.distance(self.R_TRIG, self.R_ECHO)
                if self.status == "MO":
                    break
                if e_dis < 30:
                    if self.status == "MO":
                        break
                    n_dis = self.distance(self.TRIG, self.ECHO)
                    if self.status == "MO":
                        break
                    s_dis = self.distance(self.B_TRIG, self.B_ECHO)
                    if self.status == "MO":
                        break
                    w_dis = self.distance(self.L_TRIG, self.L_ECHO)
                    if self.status == "MO":
                        break
                    if n_dis > s_dis and n_dis > w_dis:
                        if self.status == "MO":
                            break
                        self.action("N")
                        self.direction = "N"
                        if self.status == "MO":
                            break
                    elif s_dis > n_dis and s_dis > w_dis:
                        if self.status == "MO":
                            break
                        self.action("S")
                        self.direction = "S"
                        if self.status == "MO":
                            break
                    elif w_dis > n_dis and w_dis > s_dis:
                        if self.status == "MO":
                            break
                        self.action("W")
                        self.direction = "W"
                        if self.status == "MO":
                            break

            if self.status == "MO":
                break
            time.sleep(0.1)
            if self.status == "MO":
                break

    def action(self, direction):
        self.setup()

        if direction == "N":
            for l in self.logic:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.HIGH)
            #if self.status == "AUTO":
            #    t = threading.Thread(target=self.get_dis_loop)
            #    t.start()

        elif direction == "S":
            for l in self.logic:
                GPIO.output(l[0], GPIO.HIGH)
                GPIO.output(l[1], GPIO.LOW)
        elif direction == "W":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.HIGH)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
        elif direction == "E":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
        elif direction == "CWR":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
        elif direction == "ACWR":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.HIGH)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
        elif direction == "NE":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
        elif direction == "NW":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.HIGH)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
        elif direction == "SE":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
        elif direction == "SW":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
        elif direction == "TNW":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.HIGH)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
        elif direction == "TNE":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
        elif direction == "TSW":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
        elif direction == "TSE":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
        elif direction == "TSRR":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
        elif direction == "TSRL":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.HIGH)
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
        elif direction == "TNRR":
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
        elif direction == "TNRL":
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(20, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
            GPIO.output(25, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
        elif direction == "STOP":
            for l in self.logic:
                GPIO.output(l[0], GPIO.LOW)
                GPIO.output(l[1], GPIO.LOW)


if __name__ == "__main__":
    mc = MotorCar()
    while True:
        try:
            command = input("['AUTO'/'N'/'S'/'W'/'E'/'NE'/'NW'/'SE'/'SW'/'CWR'/'ACWR'/'TNW'/'TNE'/'TSW'/'TSE'/'TSRR'/'TSRL'/'TNRR'/'TNRL'/'STOP'/'EXIT']: ")
            if command.upper() == "AUTO":
                mc.p_status = mc.status
                mc.status = "AUTO"
                if mc.direction not in ["N", "S", "W", "E"]:
                    mc.action("N")
                    mc.direction = "N"
                if mc.p_status != "AUTO":
                    t = threading.Thread(target=mc.get_dis_loop)
                    t.start()
            elif command.upper() in ["N", "S", "W", "E", "NE", "NW", "SE", "SW", "CWR", "ACWR", "TNW", "TNE", "TSW", "TSE", "TSRR", "TSRL", "TNRR", "TNRL", "STOP"]:
                mc.p_status = mc.status
                mc.status = "MO"
                mc.action(command.upper())
                mc.direction = command.upper()
            elif command.upper() == "EXIT":
                break
            else:
                print("Invalid Command")
        except KeyboardInterrupt:
            break
            
    GPIO.cleanup()
