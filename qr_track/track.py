#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from imutils.video import VideoStream
from pyzbar import pyzbar
from PIL import Image
import imutils
import cv2
import requests
import json
import time
import datetime
import threading
import math
from motor import Motor
import threading
import multiprocessing
import re


class Track(object):
    def __init__(self, route_file):
        # 初始化路径文件
        self.route_file = route_file

        # 将路径坐标保存到 self.route
        self.route = {}

        # 保存读取到的 barcode 数据到 csv
        self.barcodes_file = "barcodes.csv"
        
        # 上次读取到的 barcode 数据
        self.barcode_data = None
        
        # 当前循迹状态
        self.track_status = 0

        # 上一个坐标
        self.before_coordinate = None
        
        # 当前坐标
        self.current_coordinate = None
        
        # 下一个坐标
        self.next_coordinate = None
        
        # Motor Car Action API
        self.action_api = "http://192.168.96.128:8080/api/action"

        # Motor Car Local API
        self.motor = Motor()

        # 列表保存子进程ID
        self.p_list = []

        self.init_route()

    def init_route(self):
        """
        初始化路径
        """
        path = None
        try:
            with open(self.route_file, "r") as f:
                path = f.readlines()
        except Exception as e:
            pass
        
        key = 0
        for coordinate in path:
            coordinate = coordinate.split("\n")[0].split(",")
            x = coordinate[0]
            y = coordinate[1]
            self.route[key] = (int(x), int(y))
            key = key + 1

        print("[INFO] Route {}".format(self.route))

    def get_next_direction(self):
        """
        获取下一坐标相对于当前坐标的方向和角度
        """
        before_coordinate = self.before_coordinate
        current_coordinate = self.current_coordinate
        next_coordinate = self.next_coordinate

        direction, angle = (None, None)
            
        # 计算方向
        # 假设直线 before-current 的方程式为 ax+by+c=0, a=y2-y1, b=x1-x2, c=x2y1-x1y2
        a = current_coordinate[1] - before_coordinate[1]
        b = before_coordinate[0] - current_coordinate[0]
        c = current_coordinate[0] * before_coordinate[1] - before_coordinate[0] * current_coordinate[1]

        d = a * next_coordinate[0] + b * next_coordinate[1] + c

        if d < 0:
            direction = "ACWR"
        elif d > 0:
            direction = "CWR"
        else:
            if before_coordinate[0] < current_coordinate[0]:
                if next_coordinate[0] > current_coordinate[0]:
                    direction = "N"
                    angle = 0
                else:
                    direction = "CWR"
                    angle = 180
            elif before_coordinate[0] > current_coordinate[0]:
                if next_coordinate[0] < current_coordinate[0]:
                    direction = "N"
                    angle = 0
                else:
                    direction = "CWR"
                    angle = 180
            else:
                if before_coordinate[1] < current_coordinate[1]:
                    if next_coordinate[1] > current_coordinate[1]:
                        direction = "N"
                        angle = 0
                    else:
                        direction = "ACWR"
                        angle = 180
                else:
                    if next_coordinate[1] < current_coordinate[1]:
                        direction = "N"
                        angle = 0
                    else:
                        direction = "ACWR"
                        angle = 180
            return (direction, angle)
            

        # 计算角度
        dx_bc = before_coordinate[0] - current_coordinate[0]
        dy_bc = before_coordinate[1] - current_coordinate[1]
        dx_nc = next_coordinate[0] - current_coordinate[0]
        dy_nc = next_coordinate[1] - current_coordinate[1]

        d = math.sqrt(math.pow(dx_bc, 2) + math.pow(dy_bc, 2)) * math.sqrt(math.pow(dx_nc, 2) + math.pow(dy_nc, 2))
        if d == 0:
            return (None, None)
        
        angle = math.acos((dx_bc * dx_nc + dy_bc * dy_nc) / d)
        angle = angle * 180 / math.pi    # 弧度值转角度值
        angle = 180 - angle

        return (direction, angle)

    def action(self, direction, angle=None):
        """
        通过 Motor Car 接口控制小车动作
        """
        headers = {"Content-type": "application/json"}
        command = {"command": direction}
        r = requests.post(self.action_api, data=json.dumps(command), headers=headers)
        print(r.status_code)
        print(r.text)
        if angle:
            time.sleep(angle/45)
            command = {"command": "N"}
            r = requests.post(self.action_api, data=json.dumps(command), headers=headers)

    def action_by_local(self, direction, angle=None):
        """
        本地通过 PWM 控制小车动作
        """
        self.motor.current_status = direction
        #t = threading.Thread(target=self.motor.pwm_action, args=(direction,))
        #t.start()
        
        # 终止之前的所有子进程，并清空子进程列表
        for p in self.p_list:
            p.terminate()
        self.p_list.clear()

        # 启动action子进程
        p = multiprocessing.Process(target=self.motor.pwm_action, args=(direction,))
        p.start()
        self.p_list.append(p)
        
        if angle:
            time.sleep(angle/50)
            self.motor.current_status = "N"

            #t = threading.Thread(target=self.motor.pwm_action, args=("N"))
            #t.start()

            for p in self.p_list:
                p.terminate()
            self.p_list.clear()

            p = multiprocessing.Process(target=self.motor.pwm_action, args=("N"))
            p.start()
            self.p_list.append(p)

    def go(self):
        """
        调取摄像头拍摄照片，从照片中获取含有坐标的二维码来循迹
        """
        print("[INFO] Starting video stream ....")
        vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

        csv = open(self.barcodes_file, "a")
        found = set()

        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            barcodes = pyzbar.decode(frame)

            if not barcodes:
                im = Image.fromarray(frame)
                for i in range(5):
                    im_copy = im.rotate(18+18*i)
                    barcodes = pyzbar.decode(im_copy)
                    if barcodes:
                        break

            for barcode in barcodes:
                #print("barcodes:{}".format(barcodes))
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                if barcode_type != "CODE39":
                    continue

                pattern = r"^\d-\d$"
                if not re.match(pattern, barcode_data):
                    continue

                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                text = "{} ({})".format(barcode_data, barcode_type)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # 将不重复的 barcode_data 存储到集合 found 中和 csv 文件里
                if barcode_data not in found:
                    csv.write("{},{},{}\n".format(datetime.datetime.now(), barcode_data, barcode_type))
                    csv.flush()
                    found.add(barcode_data)

                # 判断是否为重复的坐标
                if self.barcode_data == barcode_data:
                    break
                else:
                    self.barcode_data = barcode_data
                    #barcode_data_list = barcode_data.split(",")
                    barcode_data_list = barcode_data.split("-")
                    
                    x, y = (None, None)
                    try:
                        x = barcode_data_list[0]
                        y = barcode_data_list[1]
                    except:
                        continue

                    barcode_data_tuple = (int(x), int(y))

                    print("[INFO] Found barcode: {}".format(barcode_data_tuple))

                    # 初始状态
                    if self.track_status == 0 and barcode_data_tuple == self.route[self.track_status]:
                        self.before_coordinate = None
                        self.current_coordinate = self.route[self.track_status]
                        self.next_coordinate = None
                        
                        print("[STATUS] Initial Status, Route[{}]: {} was found".format(self.track_status, self.current_coordinate))
                        print("[INFO] Current Coordinate: {}".format(self.current_coordinate))
                        print("[INFO] Next Coordinate: {}".format("Searching"))

                        # 初始状态下直接往前走
                        self.action_by_local("N")
                        #self.action("N")
                        print("[INFO] Action: 'N'")
                        
                        self.track_status += 1

                    # 第二个坐标点状态 (标记点，非路径)
                    elif self.track_status == 1:
                        self.before_coordinate = self.current_coordinate
                        self.current_coordinate = barcode_data_tuple
                        self.next_coordinate = self.route[self.track_status]
                        
                        print("[STATUS] The Second Coordinate: {} was found".format(self.current_coordinate))
                        print("[INFO] Before Coordinate: {}".format(self.before_coordinate))
                        print("[INFO] Current Coordinate: {}".format(self.current_coordinate))
                        print("[INFO] Next Coordinate: {}".format(self.next_coordinate))

                        # 获取到下个坐标的方向和角度
                        direction, angle = self.get_next_direction() 
                        print("[INFO] Direction: {}".format(direction))
                        print("[INFO] Angle: {}".format(angle))
                        
                        # 控制车的动作
                        self.action_by_local(direction, angle)
                        #self.action(direction, angle)
                        print("[INFO] Action: {} Angle: {}".format(direction, angle))
                        
                        self.track_status += 1
                    
                    # 第二个坐标点之后的状态
                    elif self.track_status > 1 and barcode_data_tuple == self.next_coordinate:
                        # 判断当前坐标是否为终点
                        if self.track_status >= len(self.route):
                            self.action_by_local("STOP")
                            #self.action("STOP")
                            print("[STATUS] This is the terminal")
                        else:
                            self.before_coordinate = self.current_coordinate
                            self.current_coordinate = self.next_coordinate
                            self.next_coordinate = self.route[self.track_status]
                            
                            print("[STATUS] Route[{}]: {} was found".format(self.track_status-1, self.current_coordinate))
                            print("[INFO] Before Coordinate: {}".format(self.before_coordinate))
                            print("[INFO] Current Coordinate: {}".format(self.current_coordinate))
                            print("[INFO] Next Coordinate: {}".format(self.next_coordinate))

                            # 获取到下个坐标的方向和角度
                            direction, angle = self.get_next_direction()
                            print("[INFO] Direction: {}".format(direction))
                            print("[INFO] Angle: {}".format(angle))

                            # 控制车的动作
                            self.action_by_local(direction, angle)
                            #self.action(direction, angle)
                            print("[INFO] Action: {} Angle: {}".format(direction, angle))

                            self.track_status += 1

                    # 第二个坐标点之后的状态
                    elif self.track_status > 1 and barcode_data_tuple != self.next_coordinate:
                        self.before_coordinate = self.current_coordinate
                        self.current_coordinate = barcode_data_tuple
                        self.next_coordinate = self.next_coordinate

                        print("[STATUS] : Mark Coordinate {} was found".format(self.current_coordinate))
                        print("[INFO] Before Coordinate: {}".format(self.before_coordinate))
                        print("[INFO] Current Coordinate: {}".format(self.current_coordinate))
                        print("[INFO] Next Coordinate: {}".format(self.next_coordinate))
                        
                        # 获取到下个坐标的方向和角度
                        direction, angle = self.get_next_direction()
                        print("[INFO] Direction: {}".format(direction))
                        print("[INFO] Angle: {}".format(angle))
                        
                        # 控制车的动作
                        self.action_by_local(direction, angle)
                        #self.action(direction, angle)
                        print("[INFO] Action: {} Angle: {}".format(direction, angle))

                    
            cv2.imshow("Barcode Scanner", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        
        print("[INFO] Cleaning up ....")
        
        for p in self.p_list:
            p.terminate()
        self.p_list.clear()
        
        csv.close()
        cv2.destroyAllWindows()
        vs.stop()
        self.motor.stop()



if __name__ == "__main__":
    t = Track("./route.csv")
    t.go()

