import wifi_connect
import test4_mpu6050
import time

# 连接WiFi
wifi_connect.connect()

# 初始化mpu6050
test4_mpu6050.init_mpu6050()

# 读取数据
state = '坐姿'

sport_weight = 0
weight = 0


def device_state():
    sport_weight = 0
    sport = 0
    stand = 0
    sit = 0
    state_list = ["测试"]
    for m in range(20):
        time.sleep(0.3)
        x, y, z = test4_mpu6050.read_acceleration()

        
        if x>=0.6 and x<=3:
            if (sport_weight-y) > 0.2 or (sport_weight-y)<-0.2:
                sport +=1
            else:
                stand +=1
        else:
            sit +=1
        sport_weight = y
    return sit,stand,sport
        
        
        
        

import urequests
def report(data):
    
    # 定义目标 URL 和要发送的数据
    url = 'http://127.0.0.1:5000/'
    data = {'human_state': data}

    # 发起 HTTP POST 请求
    response = urequests.get(url)
    # response = urequests.post(url, json=data)

    # 打印服务器响应内容
    print(response.text)

    # 关闭请求连接
    response.close()



while True:
    sit,stand,sport = device_state()
    human_state = '坐姿'
    max_value = sit
    if stand > max_value:
        max_value = stand
        human_state = '站姿'
    if sport > max_value:
        max_value = sport
        human_state = '运动状态'
    report(human_state)
    print('当前状态：',human_state)




