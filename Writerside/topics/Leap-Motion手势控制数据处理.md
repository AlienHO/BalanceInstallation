# Leap Motion手势控制数据处理

## 文档介绍
- **目的**：介绍 `leap_motion_listener.py` 脚本的功能、配置和测试步骤。
- **范围**：包括脚本功能说明、环境要求、测试用例及故障排除。

## 项目概述
`leap_motion_listener.py` 是一个使用Leap Motion SDK的Python脚本，用于监听并获取Leap Motion控制器检测到的手部位置信息。

### 环境要求
- Leap Motion控制器
- Python 2.7 或 3.x
- Leap Motion SDK

### 测试用例
1. **Leap Motion SDK安装**：从Leap Motion官网下载并安装SDK。
2. **Leap Motion控制器连接**：连接Leap Motion控制器到电脑。
3. **运行脚本**：在Python环境下运行 `leap_motion_listener.py`。
4. **测试手部位置获取**：在Leap Motion控制器的感应范围内移动手部，并监视脚本输出的手部位置信息。

### 测试环境要求
- 确保Leap Motion控制器正常连接并被系统识别。
- 验证Python环境和Leap Motion SDK的安装。

## 正常运行的预期结果
- 脚本能够成功运行并初始化Leap Motion监听器。
- 当手部在Leap Motion控制器的感应范围内时，脚本应能实时输出手部的垂直位置坐标。
<video src="LEAPtest.mp4" preview-src="LEAPtest.jpg"/>



## 故障排除
- **Leap Motion控制器未识别**：检查控制器连接并确保设备驱动正确安装。
- **SDK版本不兼容**：确认已安装与Python环境兼容的Leap Motion SDK版本。
- **脚本运行错误**：检查Python环境配置，确保所有必要的库都已正确安装。
- **手部位置数据不准确**：确保Leap Motion控制器没有被遮挡，且手部在正确的感应范围内移动。
