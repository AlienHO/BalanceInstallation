# 视觉识别部分
import cv2
import numpy as np
from pythonosc import udp_client
#
import time,math,serial

import time
start_time = time.time()

def get_elapsed_time():
    """返回自程序开始以来经过的时间（以秒为单位）"""
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time

# 示例使用

# 一.设置串口连接/舵机控制
ser = serial.Serial('COM5', 9600)
time.sleep(0.5)  # 等待串口初始化

def set_servos(pos1, pos2, pos3):  
    """ 向Arduino发送命令以设置舵机位置 """
    command = f"{pos1},{pos2},{pos3}\n"
    ser.write(command.encode())

# 二.初始化舵机位置为0度
set_servos(0, 0, 0)
time.sleep(0.2)

# 三.创建变量/PID部分

    #  因为X轴和Y轴相互独立。所以使用了两套闭环系统、两套PID。所以下列变量，
    #大部分是两个元素的列表。其中第一个元素为X轴所用，第二个为Y轴所用。
比例P系数=[0.2,0.2]   #需要调参   #调好的参数：P=0.2 I=0.23 D=0.064
积分I系数=[0.23,0.23]
微分D系数=[0.064,0.064]

积分I最大值=[5,5]    #调好的参数；5

三轴映射参数=1  # 等待实际测试！！

实际距离参数=1 # 等待实际测试！！/舵机之间的距离（等边三角形边长）
画面长=320
画面宽=240
画面中点=(画面长/2,画面宽/2)

画圆移动角度=0    #手动输入
画圆移动半径=30
画圆移动速度=10 #越小越快

比例P=[0,0]   #系统自动使用的变量
积分I=[0,0]
微分D=[0,0]

偏差量=[0,0]
上一次偏差量=[0,0]

执行量=[0,0]

小球位置=[0,0]
目标量=[画面长/2,画面宽/2]

# 打开摄像头
cap = cv2.VideoCapture(0)

# OSC客户端设置
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 5005)  # OSC接收器的IP和端口

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头，请检查代码中的摄像头索引。")
    exit()

#1）Leapmotion控制部分
    
    #最终输出需求
LEAM偏转角度a=0
LEAM偏转角度b=0
LEAM偏转角度c=0


while True:
    if not cap.isOpened():
        print("无法打开摄像头，请检查代码中的摄像头索引。")
        exit()

    # 读取摄像头图像
    ret, frame = cap.read()

    # 检查帧是否成功捕获
    if not ret:
        print("无法从摄像头读取图像，请检查代码中的摄像头索引。")
        break

    # 将图像转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义黑色的颜色范围
    lower_black = np.array([0, 0, 200])
    upper_black = np.array([180, 30, 255])

    # 创建掩码
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 如果找到轮廓，则处理最大轮廓
    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        # 计算轮廓的边界矩形
        x, y, w, h = cv2.boundingRect(max_contour)

        # 绘制矩形框选识别到的物体
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 计算轮廓的中心坐标
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

            # 在图像上绘制小球的中心
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            # 在控制台输出小球的坐标
            

            # 通过OSC发送小球的坐标
            osc_client.send_message("/ball/position", [center_x, center_y])

    # 显示图像
    cv2.imshow("Frame", frame)
   
    系统运行时间 = get_elapsed_time()
    print(f"程序已运行 {系统运行时间} 秒")


    小球位置=[1,1] #2）计时/PID部分
    计时=系统运行时间
    运行时间=(系统运行时间)/1000


#3）PID计算/PID部分
    for n in range(0,2):
        偏差量[n]=目标量[n]-小球位置[n]

        比例P[n]=偏差量[n]*比例P系数[n]

        积分I[n]=积分I[n]+偏差量[n]*积分I系数[n]*运行时间

        if 积分I[n]>积分I最大值[n]:
            积分I[n]=积分I最大值[n]
        elif 积分I[n]<-积分I最大值[n]:
            积分I[n]=-积分I最大值[n]

        微分D[n]=(偏差量[n]-上一次偏差量[n])*微分D系数[n]/运行时间
        上一次偏差量[n]=偏差量[n]

        执行量[n]=比例P[n]+积分I[n]+微分D[n]

        舵机a=[0,0.577*实际距离参数] 
        舵机b=[-0.289*实际距离参数,-0.5*实际距离参数]
        舵机c=[0.289*实际距离参数,-0.5*实际距离参数]

        La=math.sqrt((执行量[0] - 舵机a[0])**2 + (执行量[1] - 舵机a[1])**2)
        Lb=math.sqrt((执行量[0] - 舵机b[0])**2 + (执行量[1] - 舵机b[1])**2)
        Lc=math.sqrt((执行量[0] - 舵机c[0])**2 + (执行量[1] - 舵机c[1])**2)

    

        PID偏转角度a=La*三轴映射参数
        PID偏转角度b=Lb*三轴映射参数
        PID偏转角度c=Lc*三轴映射参数

        自动平衡舵机偏转值=[PID偏转角度a,PID偏转角度b,PID偏转角度c] 
        Leapmotion控制偏转值=[LEAM偏转角度a,LEAM偏转角度b,LEAM偏转角度c] 
        最终输出=[0,0,0]
        
        Leapmotion接入=0 # 待设置判断leapmotion是否接入
    
        if Leapmotion接入==1:    #点触模式下，绘制两个按键的颜色框
            最终输出=Leapmotion控制偏转值
        else:
            最终输出=自动平衡舵机偏转值
    
    print(f"(执行量:{执行量})(最终输出:{最终输出})")
    time.sleep(1)


