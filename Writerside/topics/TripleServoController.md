# TripleServoController.ino 程序说明文档

## Arduino程序: TripleServoController

### 功能描述
`TripleServoController` 是一个用于控制三个伺服电机的Arduino程序。该程序使得用户可以通过串口输入来控制连接到Arduino板的三个伺服电机的角度位置。

### 硬件要求
- Arduino Uno或兼容板
- 三个伺服电机
- 连接线
- 电源（可选，取决于伺服电机的要求）

### 电路连接
- 伺服电机1连接到Arduino的数字引脚5
- 伺服电机2连接到Arduino的数字引脚6
- 伺服电机3连接到Arduino的数字引脚7

### 代码概述
1. 引入`Servo`库
2. 定义并初始化三个伺服电机对象
3. 在`setup()`函数中设置串口通信并将伺服电机对象附加到对应的引脚
4. 在`loop()`函数中，读取串口数据，并将解析得到的整数值用于设置伺服电机的位置

### 使用说明
将程序上传到Arduino板后，通过串口监视器发送三个整数值（以逗号分隔），分别对应三个伺服电机的目标位置。

---

## Python测试程序: ServoControlTest.py  {collapsible="true"}

### 功能描述
`ServoControlTest.py` 是一个Python脚本，用于自动控制`TripleServoController.ino` Arduino程序中的三个伺服电机。该脚本每秒发送一次指令，使三个伺服电机在30度和90度之间来回旋转。

### 软件要求
- Python 3.x
- `pyserial` 库
- `keyboard` 库

### 使用说明
1. 确保Arduino板已连接到计算机，并且`TripleServoController`程序已经上传并运行。
2. 运行`ServoControlTest`脚本。
3. 观察伺服电机在30度和90度之间来回旋转。
4. 按下'Q'键以退出程序。

### 程序概述
1. 初始化与Arduino的串口通信。
2. 循环发送控制信号，使伺服电机在两个预设位置之间切换。
3. 监听键盘输入，当检测到'Q'键被按下时，退出程序。

### 注意事项
- 确保修改Python脚本中的串口名称，以匹配你的系统和Arduino板的连接。
- 在某些操作系统上，可能需要管理员权限来运行Python脚本，以便使用键盘监听功能。
