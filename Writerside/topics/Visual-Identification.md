# Visual Identification 视觉识别功能配置与测试

## 概述
- `Visual-Identification.py` 是一个基于OpenCV库的Python视觉识别测试程序，用于识别图像中的特定对象（目前配置为黑色物体），并在对象周围绘制绿色矩形框。
- 此程序还能通过OSC协议发送识别对象的坐标数据。

## 环境要求
- **操作系统**：兼容Python 3.x的系统。
- **必需库**：OpenCV-python, python-osc。
- **硬件要求**：带有摄像头的计算机。

## 步骤
1. **安装Python**：访问 [Python官网](https://www.python.org/downloads/) 下载并安装Python 3.x。
2. **安装必需库**：打开命令行，执行 `pip install opencv-python python-osc`。
3. **运行程序**：确保摄像头正确连接，通过命令行或IDE运行 `python Visual-Identification.py`。
4. **程序操作**：程序运行后，自动开始图像识别并发送坐标数据。按`Q`键终止程序。

## 正常运行的预期结果
- 程序应能自动启动摄像头，识别图像中的黑色物体。
- 程序将在识别到的物体周围绘制绿色矩形框，并在物体的中心位置绘制绿点。
- 物体中心的坐标数据通过OSC协议实时发送。

<video src="Visual-Identification1.mp4" preview-src="Visual-Identification2.jpg"/>


## 故障排除
- **摄像头无法打开**：检查摄像头连接和系统识别情况。尝试修改 `cv2.VideoCapture` 中的索引值。
- **无法识别物体或发送数据**：检查Python环境和依赖库是否正确安装。确保摄像头能够捕捉到清晰的图像。
- **其他错误**：根据脚本输出的错误信息进行相应的调试和修正。