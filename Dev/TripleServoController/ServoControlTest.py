#以下是一个测试程序，用于控制三个伺服电机在30度和90度之间连续来回旋转，每间隔一秒发送一次串口信号。

import serial
import time
import keyboard  # 引入keyboard库

# 创建与Arduino的串口连接（请根据你的Arduino板子调整端口和波特率）
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def send_servo_positions(pos1, pos2, pos3):
    """
    向Arduino发送三个伺服电机的位置。
    """
    command = f"{pos1},{pos2},{pos3}\n"
    arduino.write(bytes(command, 'utf-8'))
    time.sleep(0.05) # 稍微等待以确保Arduino接收到完整的命令

def main():
    try:
        print("Press 'Q' to exit")
        while True:
            if keyboard.is_pressed('q'):  # 检查是否按下了'Q'键
                print("Exiting program")
                break

            # 发送命令让伺服电机转到30度
            send_servo_positions(30, 30, 30)
            time.sleep(1)

            # 发送命令让伺服电机转到90度
            send_servo_positions(90, 90, 90)
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        # 发送命令让伺服电机回到初始位置，并关闭串口
        send_servo_positions(0, 0, 0)
        arduino.close()

if __name__ == "__main__":
    main()
