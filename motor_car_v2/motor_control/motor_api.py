#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, request, jsonify, make_response
from motor import MotorCar
import threading
import re

#import sys
#sys.path.append("../..")
#from servo.servo_motor_v2 import ServoControl


app = Flask(__name__)
mc = MotorCar()
#sc = ServoControl()


# 小车马达控制接口
@app.route("/api/action", methods=["POST"])
def action_handle():
    """
    request json: {"command": "N"}
    """
    command = request.json.get("command")
    print(command)
    
    response = make_response(jsonify({"code": "1", "msg": "Invalid Command"}))
    
    alphabet_pattern = r"[a-zA-Z]{1,4}"    # 匹配是否为1-4个英文字母
    if re.match(alphabet_pattern, command):
        if command.upper() in ["AUTO"]:
            mc.p_status = mc.status
            mc.status = "AUTO"
            if mc.direction not in ["N", "S", "W", "E"]:
                mc.action("N")
                mc.direction = "N"
            if mc.p_status != "AUTO":
                t = threading.Thread(target=mc.get_dis_loop)
                t.start()
            response = make_response(jsonify({"code": "0", "msg": "AUTO"}))
        elif command.upper() in ["N", "S", "W", "E", "NE", "NW", "SE", "SW", "CWR", "ACWR", "TNW", "TNE", "TSW", "TSE", "TSRR", "TSRL", "TNRR", "TNRL", "STOP"]:
            mc.p_status = mc.status
            mc.status = "MO"
            mc.action(command.upper())
            mc.direction = command.upper()
            response = make_response(jsonify({"code": "0", "msg": "MO/" + command.upper()}))
        else:
            response = make_response(jsonify({"code": "1", "msg": "Invalid Command"}))
    else:
        kw_map = {"向前": "N", "前进": "N", "后退": "S", "向右走": "E", "向左走": "W", "向右前方走": "NE", "向左前方走": "NW", "向右后方走": "SE", "向左后方走": "SW", "顺时针旋转": "CWR", "逆时针旋转": "ACWR", "反转": "ACWR", "向左前方转向": "TNW", "向右前方转向": "TNE", "向左后方转向": "TSW", "向右后方转向": "TSE", "尾部顺时针转": "TNRR", "尾部逆时针转": "TNRL", "头部顺时针转": "TSRR", "头部逆时针转": "TSRL", "停止": "STOP", "自动": "AUTO"}
        
        for k in kw_map.keys():
            k_b = k.encode("utf-8")
            command_b = command.encode("utf-8")
            if re.findall(k_b, command_b):
                if k == "自动":
                    mc.p_status = mc.status
                    mc.status = "AUTO"
                    if mc.direction not in ["N", "S", "W", "E"]:
                        mc.action("N")
                        mc.direction = "N"
                    if mc.p_status != "AUTO":
                        t = threading.Thread(target=mc.get_dis_loop)
                        t.start()
                    response = make_response(jsonify({"code": "0", "msg": "AUTO"}))
                    break
                else:
                    mc.p_status = mc.status
                    mc.status = "MO"
                    mc.action(kw_map[k])
                    mc.direction = kw_map[k]
                    response = make_response(jsonify({"code": "0", "msg": "MO/" + kw_map[k]}))
                    break
            else:
                response = make_response(jsonify({"code": "1", "msg": "Invalid Command"}))
    
    # 解决跨域问题
    #response.headers["Access-Control-Allow-Origin"] = "*"
    #response.headers["Access-Control-Allow-Methods"] = "POST"
    #response.headers["Access-Control-Allow-Headers"] = "*"
    return response


# 机械臂伺服电机控制接口
#@app.route("/api/servo", methods=["POST"])
#def servo_control():
#    command = request.json.get("command")
#    value = None
#    try:
#        value = request.json.get("value")
#        value = int(value)
#    except:
#        pass
#
#    if command in ["DEFAULT", "STAND", "FORWARD", "M1", "M2", "M3", "M4", "M5"]:
#        if command in ["M1", "M2", "M3", "M4", "M5"]:
#            if value < 0 or value > 100:
#                response = make_response(jsonify({"code": "1", "msg": "Invalid value"}))
#                return response
#        sc.action(command, value)
#        response = make_response(jsonify({"code": "0", "msg": "Done"}))
#        return response
#    else:
#        response = make_response(jsonify({"code": "1", "msg": "Invalid command"}))
#        return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5566)

