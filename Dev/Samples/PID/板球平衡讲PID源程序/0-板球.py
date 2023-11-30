#作者：B站‘程欢欢的智能控制集’
#QQ群：245234784
#一、声明
import sensor, image, time,car,math
from time import sleep as 等待
from pyb import millis as 系统运行时间

#二、设置摄像头
屏幕=car.screen()
import screen_set   #对于小车屏幕的特殊设置，使屏幕反向显示
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
led=car.led()   #声明led
led.turn_on()   #打开led
sensor.skip_frames(time = 1000) #延迟1秒等待摄像头校准亮度、白平衡
sensor.set_auto_gain(False)     #关闭自动亮度
sensor.set_auto_whitebal(False) #关闭自动白平衡
sensor.set_auto_gain(False,gain_db=-100)    #降低曝光度
sensor.set_contrast(3)  #提高对比度
sensor.set_brightness(-3)   #降低亮度

clock = time.clock()#声明时钟，用于获取帧速

#三、创建常量
白球阈值=(75, 100, -20, 20, -20, 20)
画面中点=(320/2,240/2)
X轴舵机端口号=0
Y轴舵机端口号=1
X轴舵机中点=90
Y轴舵机中点=90
X轴舵机范围=(-35,35)
Y轴舵机范围=(-35,35)

#四、子函数：控制平台
舵机=car.servo_motor()    #声明舵机
def 控制平台(x,y):
    global X轴舵机端口号,Y轴舵机端口号,X轴舵机范围,Y轴舵机范围,X轴舵机中点,Y轴舵机中点
    if x<X轴舵机范围[0]:
        x=X轴舵机范围[0]
    if x>X轴舵机范围[1]:
        x=X轴舵机范围[1]
    if y<Y轴舵机范围[0]:
        y=Y轴舵机范围[0]
    if y>Y轴舵机范围[1]:
        y=Y轴舵机范围[1]
    舵机.degree(X轴舵机端口号,X轴舵机中点-x)    #x轴，向右减小
    舵机.degree(Y轴舵机端口号,Y轴舵机中点-y)    #y轴，向上增加
控制平台(0,0)   #执行一次控制平台，使平台归零

#五、创建变量
    #  因为X轴和Y轴相互独立。所以使用了两套闭环系统、两套PID。所以下列变量，
    #大部分是两个元素的列表。其中第一个元素为X轴所用，第二个为Y轴所用。
比例P系数=[0.2,0.2]   #需要调参   #调好的参数：P=0.2 I=0.23 D=0.064
积分I系数=[0.23,0.23]
微分D系数=[0.064,0.064]

积分I最大值=[5,5]    #调好的参数；5

比例P=[0,0]   #系统自动使用的变量
积分I=[0,0]
微分D=[0,0]

偏差量=[0,0]
上一次偏差量=[0,0]

执行量=[0,0]

小球位置=[0,0]
目标量=[320/2,240/2]

计时=系统运行时间()

画圆移动角度=0    #手动输入
画圆移动半径=30
画圆移动速度=10 #越小越快
模式='点触' #模式分 点触 和 自动

#六、主循环
while(True):
    clock.tick()    #用于获取帧速
#1）获取图像，并识别小球位置
    图像 = sensor.snapshot()
    小球色块们 = 图像.find_blobs([白球阈值])
    if 小球色块们:#如果找到结果
        小球色块 = max(小球色块们, key = lambda b: b.pixels())#按结果的像素值，找最大值的数据。也就是找最大的色块。
        if 小球色块.w()>20 and 小球色块.h()>20:#过滤掉长宽小于20的结果
            图像.draw_rectangle(小球色块[0:4],color=(255,0,0))#按寻找色块结果的前四个值，绘制方形，框选识别结果。
            图像.draw_cross(小球色块.cx(),小球色块.cy(),color=(255,0,0))#用结果的中心值坐标，绘制十字
            小球位置=[小球色块.cx(),小球色块.cy()]
        else:#没有找到小球
            积分I=[0,0]   #积分I清零
            小球位置=目标量 #告知系统小球达到目标，使系统停转
    else:#没有找到小球
        积分I=[0,0]   #积分I清零
        小球位置=目标量    #告知系统小球达到目标，使系统停转
#2）计时
    运行时间=(系统运行时间()-计时)/1000
    计时=系统运行时间()
#3）PID部分
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
#4）控制平台-执行量输入执行器
    控制平台(执行量[0],执行量[1])
#5）在屏幕上写字PID数值、绘制目标框
    图像.draw_string(0,0,'ERR:'+str(偏差量),color=(255,0,0))
    图像.draw_string(0,10,'P:'+str(比例P),color=(255,0,0))
    图像.draw_string(0,20,'I:'+str(积分I),color=(255,0,0))
    图像.draw_string(0,30,'D:'+str(微分D),color=(255,0,0))
    图像.draw_cross(round(目标量[0]),round(目标量[1]),thickness=3,color=(0,0,255))#用结果的中心值坐标，绘制十字
    图像.draw_cross(round(目标量[0]),round(目标量[1]),thickness=1,color=(255,255,0))#用结果的中心值坐标，绘制十字
#6）通过触屏给定目标量，或自动控制目标量画圆
    屏幕.get_touch()  #获取触屏数据
    if 屏幕.touch_exist():    #如果存在触摸
        if 48<屏幕.touch_x()<80 and 200<屏幕.touch_y()<240: #触摸坐标在第一个按键内
            模式='自动'
        elif 0<屏幕.touch_x()<40 and 200<屏幕.touch_y()<240:#触摸坐标在第二个按键内
            模式='点触'
        elif 模式=='点触':  #点触模式下，根据触摸改变目标点位置。因为屏幕倒置，所以坐标需要反向
            目标量=[320-屏幕.touch_x(),240-屏幕.touch_y()]

    if 模式=='点触':    #点触模式下，绘制两个按键的颜色框
        图像.draw_rectangle(280,0,40,40,thicness=2,color=(0,255,0))
        图像.draw_rectangle(239,0,40,40,thicness=2,color=(255,0,0))
    elif 模式=='自动':  #自动模式下，绘制两个按键的颜色框
        图像.draw_rectangle(280,0,40,40,thicness=2,color=(255,0,0))
        图像.draw_rectangle(239,0,40,40,thicness=2,color=(0,255,0))
        #通过三角函数，让目标量以画形轨迹移动。反斜杠是换行符，自动连接上下两行语句
        目标量=[画圆移动半径*math.cos(画圆移动角度)+画面中点[0],\
                画圆移动半径*math.sin(画圆移动角度)+画面中点[1]]
        画圆移动角度+=math.pi/画圆移动速度  #累加角度。注意程序使用弧度制表示角度。
        if 画圆移动角度>math.pi*2:    #角度达到一圈后归零。
            画圆移动角度=0

#7）显示图像到屏幕
    屏幕.display(图像)  #在屏幕上显示图像
    print(clock.fps())  #打印帧速
