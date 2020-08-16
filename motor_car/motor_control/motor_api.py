#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, request, jsonify, make_response
from motor import MotorCar


app = Flask(__name__)
mc = MotorCar()

@app.route("/api/action", methods=["POST"])
def action_handle():
    """
    request json: {"command": "N"}
    """
    command = request.json.get("command")
    print(command)
    if command.upper() in ["AUTO", "自动模式"]:
        t_p_status = mc.status
        mc.status = "AUTO"
        mc.action("N", t_p_status)
        response = make_response(jsonify({"code": "0", "msg": "AUTO/N"}))
    elif command.upper() in ["N", "S", "W", "E", "P", "前进", "后退", "右转", "左转", "停止"]:
        mc.status = "MO"
        km = {"前进": "N", "后退": "S", "右转": "E", "左转": "W", "停止": "P", "N": "N", "S": "S", "W": "W", "E": "E", "P": "P"}
        mc.action(km[command.upper()])
        response = make_response(jsonify({"code": "0", "msg": "MO/" + km[command.upper()]}))
    else:
        response = make_response(jsonify({"code": "1", "msg": "Invalid Command"}))
    
    # 解决跨域问题
    #response.headers["Access-Control-Allow-Origin"] = "*"
    #response.headers["Access-Control-Allow-Methods"] = "POST"
    #response.headers["Access-Control-Allow-Headers"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5566)
