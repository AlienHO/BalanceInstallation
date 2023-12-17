# 一.前置

# 00)导入库
import cv2
import numpy as np
from pythonosc import udp_client
import time,math,serial



# 01)时间变量（存在出错可能性）
last_time = time.time()
start_time = time.time()

def get_elapsed_time():
    """返回自程序开始以来经过的时间（以秒为单位）"""
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time


# 03)设置串口连接/舵机控制
try:
    ser = serial.Serial('/dev/tty.usbserial-110', 9600)
    serial_port_available = True
    time.sleep(0.5)  # 等待串口初始化
except serial.SerialException:
    serial_port_available = False
    print("无法打开串口，将使用模拟数据。")

def set_servos(pos1, pos2, pos3):  
    """ 向Arduino发送命令以设置舵机位置，或模拟发送命令 """
    command = f"{pos1},{pos2},{pos3}\n"
    if serial_port_available:
        ser.write(command.encode())
    else:
        print(f"模拟发送数据: {command}")

    
    # 初始化舵机位置为0度
set_servos(0, 0, 0)
time.sleep(0.2)


# 04)摄像头启动
cap = cv2.VideoCapture(0)
    
    # 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头，请检查代码中的摄像头索引。")
    exit()


# 05)OSC客户端设置
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 5005)  # OSC接收器的IP和端口


# 二.创建变量/PID部分

    # 因为X轴和Y轴相互独立。所以使用了两套闭环系统、两套PID。所以下列变量，
    #大部分是两个元素的列表。其中第一个元素为X轴所用，第二个为Y轴所用。

# 01)PID比例系数
比例P系数=[0.2,0.2]   #需要调参   #调好的参数：P=0.2 I=0.23 D=0.064
积分I系数=[0.23,0.23]
微分D系数=[0.064,0.064]
积分I最大值=[5,5]    #调好的参数；5

# 02)重要常量（需要实际测量）
    #以画面左上角为坐标轴原点

画面长=1400
画面宽=890
    
    # 重要参数！！！，PID预设范围
预设范围=140
    
    #若设舵机最大偏转角度为70
PID偏转系数=70/预设范围

# 03)系统自动使用的变量
比例P=[0,0]   
积分I=[0,0]
微分D=[0,0]

偏差量=[0,0]
上一次偏差量=[0,0]

执行量=[0,0]

小球位置=[0,0]
目标量=[画面长/2,画面宽/2]



# ！主循环部分！
while True:
    
    系统运行时间 = get_elapsed_time()
    print(f"程序已运行 {系统运行时间} 秒")


# 二.视觉识别部分

    # 01)读取摄像头图像
    ret, frame = cap.read()

    # 02)检查帧是否成功捕获
    if not ret:
        print("无法从摄像头读取图像，请检查代码中的摄像头索引。")
        break

    # 03)将图像转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 定义两个正红色的颜色范围
        # 第一个范围捕捉低色调的红色
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

        # 第二个范围捕捉高色调的红色
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

        # 创建两个掩码并合并
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # 04)查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 05)如果找到轮廓，则处理最大轮廓
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

            # 通过OSC发送小球的坐标
            osc_client.send_message("/ball/position", [center_x, center_y])
            
            小球位置=[center_x,center_y]



# 三.Leapmotion控制部分
    
    # 01)LEAP接入与输入
    x轴控制=300     #防报错预设
    y轴控制=300     #防报错预设
    LEAP原始输入值=[x轴控制,y轴控制]
    
    # 02)LEAP输入值范围
    最大=250    #防报错预设
    最小=500    #防报错预设
    LEAP输入有效范围=[最大,最小]
    LEAP有效输入值 = [value - 最大 if value > 最大 else (最小 if value == 最小 else value) for value in LEAP原始输入值]

    # 03)LEAP转化为三轴偏转
    LEAP范围=最大-最小 #需要实际估测！！
    C=LEAP范围

    # 04)若以为LEAP范围基准建立直角坐标系，可得为（LEAP范围，LEAP范围），舵机等边三角形，呈倒三角居中
            # 等边三角形边长=预设范围*2
    
        # LEAP居中偏移量D
    D=C*(1-0.886)/2
    
    LEAP舵机a=[D,0]
    LEAP舵机b=[D,C]
    LEAP舵机c=[D+0.866*C,C/2]
        
    # 05)将小球位置映射在执行量坐标系中
        
    LEAP小球位置映射系数=C/画面宽
    LEAP映射坐标 = [LEAP小球位置映射系数 * 小球位置[0], LEAP小球位置映射系数 * 小球位置[1]]

        
    # 06)计算在映射坐标系中，小球与舵机位置的距离
    LEAP球舵距离a=math.sqrt((LEAP映射坐标[0] - LEAP舵机a[0])**2 + (LEAP映射坐标[1] - LEAP舵机a[1])**2)
    LEAP球舵距离b=math.sqrt((LEAP映射坐标[0] - LEAP舵机b[0])**2 + (LEAP映射坐标[1] - LEAP舵机b[1])**2)
    LEAP球舵距离c=math.sqrt((LEAP映射坐标[0] - LEAP舵机c[0])**2 + (LEAP映射坐标[1] - LEAP舵机c[1])**2)
        
    LEAP球舵距离=[LEAP球舵距离a,LEAP球舵距离b,LEAP球舵距离c]
    
    # 07)得出偏转角度，若设舵机最大偏转角度为70，则LEAP偏转系数为 70/范围内最大值

    LEAP偏转系数=70/最大

    LEAP偏转角度a=int(LEAP球舵距离a*LEAP偏转系数)
    LEAP偏转角度b=int(LEAP球舵距离b*LEAP偏转系数)
    LEAP偏转角度c=int(LEAP球舵距离c*LEAP偏转系数)

# 四.PID控制部分
    for n in range(0,2):
        
        # 01)计时（可能出错）
        计时=系统运行时间
        运行时间=(系统运行时间)/1000
        
        # 02)PID核心
        偏差量[n]=目标量[n]-小球位置[n]

        比例P[n]=偏差量[n]*比例P系数[n]

        积分I[n]=积分I[n]+偏差量[n]*积分I系数[n]*运行时间

        if 积分I[n]>积分I最大值[n]:
            积分I[n]=积分I最大值[n]
        elif 积分I[n]<-积分I最大值[n]:
            积分I[n]=-积分I最大值[n]

        微分D[n]=(偏差量[n]-上一次偏差量[n])*微分D系数[n]/运行时间
        上一次偏差量[n]=偏差量[n]

        # 02)执行量输出
        # 计算执行量的新值
        新执行量 = 比例P[n] + 积分I[n] + 微分D[n]

        # 03)估测执行量范围为（-70,70），将执行量转化为以左上角为（0,0）
        
        预设范围=140 #需要实际估测！！
        A=预设范围
        
        # 将执行量的新值转化为以左上角为（0,0）的坐标系
        执行量[n] = int(新执行量 + A/2)

        # 04)若以执行量为基准建立直角坐标系，可得为（140，140），舵机等边三角形，呈倒三角居中
            # 等边三角形高=预设范围
            # 居中偏移量B
        B=0
        舵机a=[B,0]
        舵机b=[B+A/0.886,0]
        舵机c=[B+A/0.886/2,A]
        
        

        # 05)将小球位置映射在执行量坐标系中
        
        小球位置映射系数=A/画面宽
        映射坐标 = [小球位置映射系数 * 小球位置[0], 小球位置映射系数 * 小球位置[1]]
        
        # 06)计算在映射坐标系中，小球与舵机位置的距离
        球舵距离a=math.sqrt((映射坐标[0] - 舵机a[0])**2 + (映射坐标[1] - 舵机a[1])**2)
        球舵距离b=math.sqrt((映射坐标[0] - 舵机b[0])**2 + (映射坐标[1] - 舵机b[1])**2)
        球舵距离c=math.sqrt((映射坐标[0] - 舵机c[0])**2 + (映射坐标[1] - 舵机c[1])**2)
        
        球舵距离=[球舵距离a,球舵距离b,球舵距离c]
    
        # 07)小球与舵机之间距离越大，舵机应偏转越大  
        PID偏转角度a=int(球舵距离a*PID偏转系数)
        PID偏转角度b=int(球舵距离b*PID偏转系数)
        PID偏转角度c=int(球舵距离c*PID偏转系数)
        
        # 08)最终输出
        最终输出=[0,0,0]
        
        PID偏转值=[PID偏转角度a,PID偏转角度b,PID偏转角度c] 
        LEAP偏转值=[LEAP偏转角度a,LEAP偏转角度b,LEAP偏转角度c] 
        
        # 09）采用何种方式控制
        LEAP接入=0 # 待设置判断leapmotion是否接入
    
        if LEAP接入==1:    
            最终输出=LEAP偏转值
        else:
            最终输出=PID偏转值
    
    # 五.串口输出
    set_servos(最终输出[0],最终输出[1],最终输出[2])
    
    # 六.输出检测，非常重要，用于检测数据转换出现问题的位置
    
    print(f"{小球位置}(执行量:{执行量})(舵机距离:{球舵距离})(最终输出:{最终输出})")
        # 在主循环的视觉识别部分和PID控制部分之间添加以下代码
# 转换舵机坐标到图像坐标系
# 假设逻辑坐标系和图像坐标系有直接的线性关系，这需要根据您的实际情况调整

    def 舵机坐标到图像坐标(舵机坐标):
    # 这里的转换系数需要根据您的实际摄像头视场和舵机位置调整
        图像坐标转换系数x = 画面长 / 220
        图像坐标转换系数y = 画面宽 / 预设范围
        return [int(舵机坐标[0] * 图像坐标转换系数x), int(舵机坐标[1] * 图像坐标转换系数y)]

# 转换舵机a, b, c的坐标
    舵机a图像坐标 = 舵机坐标到图像坐标(舵机a)
    舵机b图像坐标 = 舵机坐标到图像坐标(舵机b)
    舵机c图像坐标 = 舵机坐标到图像坐标(舵机c)

# 绘制舵机位置
    cv2.circle(frame, (舵机a图像坐标[0], 舵机a图像坐标[1]), 5, (255, 0, 0), -1) # 舵机a
    cv2.circle(frame, (舵机b图像坐标[0], 舵机b图像坐标[1]), 5, (255, 0, 0), -1) # 舵机b
    cv2.circle(frame, (舵机c图像坐标[0], 舵机c图像坐标[1]), 5, (255, 0, 0), -1) # 舵机c

# 接下来是cv2.imshow("Frame", frame)的代码
    
    # 06)显示图像   
    cv2.imshow("Frame", frame)
    
    # 07)检测键盘按键，如果按下'q'键，则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 显示更新后的图像
# cv2.imshow("Frame with Servo Positions", frame)

    

# 关闭摄像头和窗口
cap.release()
cv2.destroyAllWindows()
