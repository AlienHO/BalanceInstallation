# TripleServoController 电机转动功能配置和测试

## 概述
`TripleServoController` 是一个用于控制三个伺服电机的Arduino测试程序。本指南提供程序的配置和测试步骤，确保伺服电机可以正常运行，并提供故障排除的指导。

## 环境要求
- Arduino Uno或兼容板
- 三个伺服电机
- 连接线
- 电源
- Python 3.x

## 步骤
1. **硬件连接**：按照以下方式连接伺服电机至Arduino和外接电源(外接电源一定要和Arduino板共地)：
   ![](schematic.png)
2. **程序上传**：将`TripleServoController.ino`程序上传到Arduino板。
3. **串口监视**：打开串口监视器，发送三个整数值（以逗号分隔），分别设置三个伺服电机的目标位置。
4. **测试脚本运行**：确保已安装Python及相关库，运行`ServoControlTest.py`脚本自动测试伺服电机。

## 正常运行的预期结果
- 伺服电机应按照串口输入的指令旋转到指定位置。
- 测试脚本应使伺服电机在30度和90度之间来回旋转。
<video src="ServoTest.mp4" preview-src="ServoTest.jpg"/>


## 故障排除
- [舵机无法正常运行（已解决）](ErrorReport.md)
- **串口通信问题**：检查Arduino的串口连接是否正确。
- **电机响应问题**：确保伺服电机电源供应充足，检查连接线是否稳固。
- **程序问题**：确认Arduino程序和Python脚本是否正确无误。
- **硬件故障**：检查伺服电机和Arduino板是否有损坏或接触不良。