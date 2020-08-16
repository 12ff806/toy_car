#!/usr/bin/env python3


import serial
import time


ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=None)
if ser.isOpen():
    print("open")

while True:
    try:
        data = ser.read()
        time.sleep(0.08)
        remaining_bytes = ser.inWaiting()
        data += ser.read(remaining_bytes)
        data = list(data)
        roll = ((data[25]<<8)|data[24])/32768*180
        pitch = ((data[27]<<8)|data[26])/32768*180
        yaw = ((data[29]<<8)|data[26])/32768*180
        print("length: {}, data: {}".format(len(data), data))
        print("roll: {}, pitch: {}, yaw: {}\n".format(roll, pitch, yaw))
    except Exception as e:
        print("Exception:", e)

