# 视觉识别功能配置与测试

## 文档介绍
- **目的**：介绍 `Visual-Identification.py` 视觉识别测试程序的配置与测试流程。
- **范围**：涵盖程序的安装、运行、预期结果以及故障排除。

## 项目概述
- `Visual-Identification.py` 是一个基于OpenCV库的Python视觉识别测试程序，主要用于识别图像中的黑色物体，并绘制绿色矩形框。同时，程序通过OSC协议发送识别对象的坐标数据。

### 环境要求
- **操作系统**：兼容Python 3.x的系统。
- **必需库**：OpenCV-python, python-osc。
- **硬件要求**：带有摄像头的计算机。

### 测试用例
1. **安装Python**：访问 [Python官网](https://www.python.org/downloads/) 下载并安装Python 3.x。
2. **安装必需库**：通过命令行执行 `pip install opencv-python python-osc`。
3. **运行程序**：确保摄像头正确连接，通过命令行或IDE运行 `python Visual-Identification.py`。
4. **程序操作**：程序启动后，自动进行图像识别并发送坐标数据。按`Q`键终止程序。

### 测试环境要求
- 确保操作系统和必需的库安装正确。
- 验证摄像头的连接和功能。

## 正常运行的预期结果
- 程序成功启动摄像头，准确识别图像中的黑色物体。
- 在识别物体周围绘制绿色矩形框，物体中心绘制绿点。
- 物体中心坐标数据通过OSC协议实时发送。
<video src="Visual-Identification1.mp4" preview-src="Visual-Identification2.jpg"/>


## 故障排除
- **摄像头无法打开**：检查摄像头连接和系统识别。尝试调整 `cv2.VideoCapture` 的索引值。
- **无法识别物体或发送数据**：核实Python环境和库的安装状况。确保摄像头能够捕获清晰图像。
- **其他错误**：根据程序输出的错误信息进行调试和修正。

