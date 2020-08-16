## 简介

用树莓派3B+制作的玩具车

## 材料清单

* raspberry pi 3B+ * 1
* 麦克纳姆轮 * 4
* 电机驱动器L298N * 2
* 直流电机及电机固定器 * 4
* HC-SR04超声波模块 * 4
* 充电宝 * 1 (给树莓派供电)
* USB线 * 1 (树莓派供电线)
* 5号电池 * 4 (给电机供电)
* 电池盒 * 1
* 透明亚克力板 * 2
* 铜柱 若干
* 杜邦线 若干
* 螺丝 若干

## 效果图

![](/docs/statics/toy_car_view_1.jpg)
![](/docs/statics/toy_car_view_3.jpg)
![](/docs/statics/toy_car_view_2.jpg)

## 麦克纳姆轮安装及工作原理

![](/docs/statics/directions.png)

## 接线

电机驱动器使能:

* GPIO 2

电机驱动器与树莓派接线:

* GPIO 20, GPIO 21  左前轮
* GPIO 12, GPIO 13  右前轮
* GPIO 22, GPIO 25  左后轮
* GPIO 26, GPIO 27  右后轮

超声波模块与树莓派接线:

* GPIO 17 (TRIG), GPIO 18 (ECHO)  前
* GPIO 23 (TRIG), GPIO 24 (ECHO)  左
* GPIO 16 (TRIG), GPIO 19 (ECHO)  右
* GPIO 5 (TRIG), GPIO 6 ECHO()  后

## 代码说明

~~~sh
├── LICENSE
├── README.md
├── docs
├── motor_car       非麦克纳姆轮版本
├── motor_car_v2    本项目用此版本代码
├── motor_car_v3    使用霍尔测速电机版本
├── motor_car_v4    使用姿态传感器版本
└── qr_track        二维码循迹版本
~~~

## 部署及运行

* [部署及运行](/docs/motor_car.md)

## 手机控制

![](/docs/statics/action_control.png)

