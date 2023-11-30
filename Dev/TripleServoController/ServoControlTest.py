#以下是一个测试程序，控制上面arduino程序的这三个舵机。该程序首先将舵机默认设置为0度，然后让它们同时旋转到60度，接着旋转到160度，然后回到0度，并重复这个过程5次。
import serial
import time

# 设置串口连接
ser = serial.Serial('/dev/tty.usbmodem1101', 9600)
time.sleep(0.5)  # 等待串口初始化

def set_servos(pos1, pos2, pos3):
    """ 向Arduino发送命令以设置舵机位置 """
    command = f"{pos1},{pos2},{pos3}\n"
    ser.write(command.encode())

# 初始化舵机位置为0度
set_servos(0, 0, 0)
time.sleep(0.5)

for _ in range(5):
    # 设置舵机到60度
    set_servos(60, 60, 60)
    time.sleep(0.5)

    # 设置舵机到160度
    set_servos(90, 90, 90)
    time.sleep(0.5)

    # 重置舵机到0度
    set_servos(0, 0, 0)
    time.sleep(0.5)

ser.close()  # 关闭串口连接
