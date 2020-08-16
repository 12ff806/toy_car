#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import serial
import time


class Motion(object):
    """
    获取姿态传感器数据
    """
    def __init__(self):
        # 初始化串口
        self.ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=None)
        #self.yaw = None

    def get_yaw(self):
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
                
                yaw = ((data[29]<<8)|data[26])/32768*180
                #print(yaw)
                #self.yaw = yaw
                return yaw
            except Exception as e:
                print("Exception:", e)
                #self.ser.close()


if __name__ == "__main__":
    m = Motion()
    print(m.get_yaw())
    #print(m.yaw)

