from machine import Pin, I2C
import time

# 定义MPU6050的I2C地址和相关寄存器地址
MPU6050_ADDR = 0x68
MPU6050_PWR_MGMT_1 = 0x6B
MPU6050_ACCEL_CONFIG = 0x1C
MPU6050_ACCEL_XOUT_H = 0x3B

# 初始化I2C总线
i2c = I2C(scl=Pin(22), sda=Pin(21))

# 初始化MPU6050模块
def init_mpu6050():
    i2c.writeto_mem(MPU6050_ADDR, MPU6050_PWR_MGMT_1, b'\x00')  # 唤醒MPU6050
    i2c.writeto_mem(MPU6050_ADDR, MPU6050_ACCEL_CONFIG, b'\x08')  # 设置加速度量程为±4g

# 读取加速度传感器数据并转换为g值
def read_acceleration():
    data = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_XOUT_H, 6)
    x = (data[0] << 8 | data[1]) / 8192.0  # 8192是±4g量程下的刻度因子
    y = (data[2] << 8 | data[3]) / 8192.0
    z = (data[4] << 8 | data[5]) / 8192.0
    return x, y, z

# 主程序
def main():
    init_mpu6050()

    while True:
        x, y, z = read_acceleration()
        print("Acceleration (g) - X:", x, "Y:", y, "Z:", z)
        time.sleep(1)  # 每秒读取一次数据

if __name__ == "__main__":
    main()
