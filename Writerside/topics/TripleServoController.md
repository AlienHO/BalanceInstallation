# TripleServoController.ino 程序说明文档

- [ErrorReport-大型舵机串口控制异常及电源问题](ErrorReport.md)

![](schematic.png)
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

## 测试程序: ServoControlTest.py  {collapsible="true"}

### 功能描述
`ServoControlTest.py` 是一个Python脚本，用于自动控制`TripleServoController.ino` Arduino程序中的三个伺服电机。使三个伺服电机在30度和90度之间来回旋转。

### 软件要求
- Python 3.x
- `pyserial` 库
- `keyboard` 库

### 使用方法
- 确保已经安装Python和pyserial库。
- 将Arduino设备通过USB连接到计算机。
- 确认Arduino设备的串口名称（在本脚本中为/dev/tty.usbmodem1101）。
- 运行脚本。脚本会自动通过串口与Arduino设备通信，控制连接的舵机。

### 程序概述
- 将所有三个舵机初始化到0度位置。
- 循环五次，每次循环中：
- 将所有舵机旋转到60度。
- 然后旋转到90度。
- 最后将舵机回旋到0度初始位置。

### 注意事项
- 确保修改Python脚本中的串口名称，以匹配你的系统和Arduino板的连接。
- 确保Arduino设备已正确编程，能够解析并响应发送到其串口的位置指令。
- 如果舵机或Arduino设备在使用过程中出现问题，可能需要检查电源供应或硬件连接。