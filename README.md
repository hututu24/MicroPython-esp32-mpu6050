# MicroPython-esp32-mpu6050
在esp32上使用MicroPython完成配网，读取mpu6050的数据，简单处理后将数据上传到服务器

1、此模块main文件中并无文件，您需从test_main.py开始执行，模块如果联网失败后会主动切换到ap模式，您需要连接热点后访问192.168.4.1输入您想将模块连接到的WiFi账号以及密码。
2、输入完成后，模块将自动重启，再次执行连接WiFi代码，若失败则将继续执行第一条
3、本模块使用iic协议连接mpu6050，若您需要将其数据上传到服务器，请您在test_main.py中配置您的服务器ip及端口，esp32将以http请求将数据post到您的服务器上

## 关于test4_mpu6050.py
您可以连接好scl=Pin(22), sda=Pin(21)，以及vcc、gnd线后，在Thonny中直接运行test4_mpu6050.py文件，将会打印出实时的加速度信息
