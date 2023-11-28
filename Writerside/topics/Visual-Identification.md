
# Visual-Identification.py 程序说明文档

## 概述
- `Visual-Identification.py` 是一个使用OpenCV库的Python视觉识别脚本。[OpenCV官方文档](https://docs.opencv.org/3.4/d2/d96/tutorial_py_table_of_contents_imgproc.html)
- 其主要功能是通过摄像头捕捉图像，识别图像中的特定对象（现已改为黑色物体），并在对象周围绘制绿色的矩形框。
- 脚本现在还包括使用OSC协议发送识别对象的坐标数据。

<video src="Visual-Identification1.mp4" preview-src="Visual-Identification2.jpg"/>
## 需求
- **环境**：Python 3.x
- **依赖库**：OpenCV-python, python-osc
- **硬件**：配备摄像头的计算机

## 安装指南
1. 安装Python 3.x: 访问 [Python官网](https://www.python.org/downloads/) 并根据您的操作系统下载并安装Python。
2. 安装OpenCV和python-osc: 打开命令行工具，输入以下命令：
   ```bash
   pip install opencv-python python-osc
   ```

## 使用说明
1. 确保摄像头已正确连接并能被操作系统识别。
2. 通过命令行或IDE运行脚本：
   ```bash
   python Visual-Identification.py
   ```
3. 脚本将自动打开摄像头，并开始识别图像中的黑色物体，并通过OSC发送坐标数据。
4. 如需终止程序，请在脚本运行的窗口中按下`Q`键。

## 代码结构
- **摄像头处理**：使用OpenCV函数 `VideoCapture` 打开并读取摄像头的视频流。
- **颜色识别**：将捕获的图像转换为HSV颜色空间，并定义了黑色的颜色范围。
- **对象识别**：根据定义的颜色范围创建掩码，然后在掩码上找到图像的轮廓。
- **轮廓处理**：计算最大轮廓的边界矩形，并绘制绿色矩形框标记。
- **中心坐标计算和传输**：计算并标注轮廓的中心坐标，通过OSC协议发送坐标数据。

## 错误处理
- 如果摄像头无法打开，脚本会输出错误消息，并终止运行。
- 对于读取摄像头时的常见错误，脚本同样会输出相应的错误消息。



## 代码解释

### 导入必要的库
```python
import cv2
import numpy as np
from pythonosc import udp_client
```
- 导入了OpenCV库和numpy库进行图像处理。
- 导入了python-osc库用于OSC通信。

### 摄像头初始化
```python
cap = cv2.VideoCapture(0)
```
- `cv2.VideoCapture(0)` 初始化摄像头。`0` 是摄像头的默认索引，通常指向系统的主摄像头。
- 如果使用 `cv2.VideoCapture(0)` 无法正常初始化摄像头，可以尝试使用 `cv2.VideoCapture(1)`。`1` 是备用索引，适用于多摄像头系统或当默认摄像头索引不起作用时。
- 在不同的系统或硬件配置中，摄像头的索引可能会有所不同。如果以上两个选项都无法工作，可能需要检查系统设置或文档以确定正确的摄像头索引。

### OSC客户端初始化
```python
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
```
- 初始化OSC客户端，设置目标IP地址和端口，用于发送数据。

### 主循环
```python
while True:
    # ...
```
- 程序进入一个无限循环，持续读取摄像头的图像并进行处理。

### 读取和处理图像
```python
ret, frame = cap.read()
# ...
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# ...
mask = cv2.inRange(hsv, lower_black, upper_black)
# ...
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```
- 捕获摄像头的每一帧。
- 将图像从 BGR 转换为 HSV 颜色空间。
- 创建一个掩码以识别黑色物体。
- 查找图像中的轮廓。

### 绘制矩形和中心点、发送信息
```python
if contours:
    # ...
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
    osc_client.send_message("/ball/position", [center_x, center_y])
```
- 在识别到的物体周围绘制绿色矩形框。
- 在物体的中心绘制一个绿点。
- 通过OSC发送识别到的物体中心点的坐标。

### 结束程序
```python
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
# ...
cap.release()
cv2.destroyAllWindows()
```
- 检测 'Q' 键按下以退出循环。
- 释放摄像头资源并关闭所有 OpenCV 窗口。
