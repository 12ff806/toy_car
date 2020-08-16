## 简介

toy car


## 部署

### 安装依赖

~~~sh
python3 -m venv venv    # 创建虚拟环境
. ./venv/bin/activate    # 激活虚拟环境
pip install -r requirements.txt -i https://pypi.douban.com/simple    # 安装依赖包
~~~

### 启动web接口(0.0.0.0:5566)

~~~sh
pip install gunicorn    # 安装gunicorn
gunicorn motor_api:app -c ./gunicorn_config.py >> ./logs/extra.log 2>&1 &    # 启动gunicorn
~~~

### 安装nginx

~~~sh
apt-get install nginx    # 安装nginx
~~~

### 配置nginx

起一个8080口作为反向代理，处理跨域问题，配置如下：

~~~sh
server {
    listen 8080;
    server_name _;

    location / {
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
        add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        proxy_pass http://127.0.0.1:5566;
    }
}
~~~

### 部署前端页面

起一个80口访问前端操作页面，将前端页面copy到目录"/var/www/html"下，并配置nginx如下：

~~~sh
server {
    listen 80;
    server_name _;

    location / {
        root /var/www/html;
    }
}
~~~

### 运行

系统重启后，nginx会自动启动，还需手动启动web接口服务。

~~~sh
. ./venv/bin/activate    # 激活虚拟环境
gunicorn motor_api:app -c ./gunicorn_config.py >> ./logs/extra.log 2>&1 &    # 启动gunicorn
~~~

树莓派ip变化后，手机访问地址改为变化后的局域网ip地址，并将/var/www/html/js/motor.js里的请求ip更换为当前ip


## 接口文档

请求方式通过`HTTP`方式进行通讯，`POST`方式传递参数，参数的编码格式采用`UTF-8`编码格式。

### 1.1、接口地址

~~~sh
http://192.168.96.130:8080/api/action    (局域网ip地址会变化)
~~~

### 1.2、接口类型

`POST` & `application/json`

### 1.3、入参模板

```json
{
  "command": "N"
}
```

### 1.4、入参介绍

|参数名|参数类型|必填|参数说明|示例|
|------|------|-------|----|-------|
|command|字符串|是|控制指令|"前进"/"N", "后退"/"S", "向右走"/"E", "向左走"/"W", "向右前方走"/"NE", "向左前方走"/"NW", "向右后方走"/"SE", "向左后方走"/"SW", "顺时针旋转"/"CWR", "逆时针旋转"/"ACWR", "向左前方转向"/"TNW", "向右前方转向"/"TNE", "向左后方转向"/"TSW", "向右后方转向"/"TSE", "尾部顺时针转"/"TNRR", "尾部逆时针转"/"TNRL", "头部顺时针转"/"TSRR", "头部逆时针转"/"TSRL", "停止"/"STOP"|

### 1.5、出参模板

成功请求返回示例

```json
{
  "code": "0",
  "msg": "AUTO/N"
}
```

失败请求返回示例

```json
{
  "code": "1",
  "msg": "Invalid Command"
}
```

### 1.6 出参介绍

|参数名|参数类型|必填|参数说明|示例|
|------|------|-------|----|-------|
|code|字符串|是|状态码 "0" 成功 "1" 失败|"0"|
|msg|字符串|是|当前小车的状态信息或请求失败原因 "AUTO/N" 自动模式 前进 "MO/N" 手动模式 前进 |"MO/P"|

