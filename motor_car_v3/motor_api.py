#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, request, jsonify, make_response
from motor import MotorCar
import threading
import re


app = Flask(__name__)
mc = MotorCar()


# 小车马达控制接口
@app.route("/api/action", methods=["POST"])
def action_handle():
    """
    request json: {"command": "N"}
    """
    command = request.json.get("command")
    print(command)
    
    response = make_response(jsonify({"code": "1", "msg": "Invalid Command"}))
    
    alphabet_pattern = r"[a-zA-Z]{1,6}"    # 匹配是否为1-6个英文字母
    if re.match(alphabet_pattern, command):
        if command.upper() in ["N", "S", "CWR", "ACWR", "TNR", "TNL", "TSR", "TSL", "STOP"]:
            mc.action(command.upper())
            response = make_response(jsonify({"code": "0", "msg": command.upper()}))
        elif command.upper() in ["STATUS"]:
            r_direction, r_speed, l_direction, l_speed = mc.get_current_status()
            response = make_response(jsonify({"code": "0", "msg": {"right_direction": r_direction, "right_speed": r_speed, "left_direction": l_direction, "left_speed": l_speed}}))
        elif command.upper() in ["SPEED"]:
            value = None
            try:
                value = request.json.get("value")
                value = int(value)
            except:
                response = make_response(jsonify({"code": "1", "msg": "Invalid Value"}))
            
            if value >= 20 and value <= 100:
                mc.set_pwm_value(value)
                response = make_response(jsonify({"code": "0", "msg": {"PWM": value}}))
            else:
                response = make_response(jsonify({"code": "1", "msg": "Invalid Value"}))
    else:
        response = make_response(jsonify({"code": "1", "msg": "Invalid Command"}))
    
    # 解决跨域问题
    #response.headers["Access-Control-Allow-Origin"] = "*"
    #response.headers["Access-Control-Allow-Methods"] = "POST"
    #response.headers["Access-Control-Allow-Headers"] = "*"
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5566)

