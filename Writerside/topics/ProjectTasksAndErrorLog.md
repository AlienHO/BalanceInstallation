# 项目任务与错误日志

### 系统设计 Development 

| TaskID | Description                                   | Status  | Errors                                                                                                                                                         |
|--------|-----------------------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | [视觉识别功能配置与测试](Visual-Identification.md)       | Done    | [摄像头无法打开(Done)](Visual-Identification.md#A)<br/>[无法识别物体或发送数据(Done)](Visual-Identification.md#A)                                                                |
| 1      | [实现PID控制算法](PID.md)                           | Done    | [硬件连接问题(Done)](PID.md#A)<br/>[PID参数不当(Done)](PID.md#A)                                                                                                         |
| 2      | [电机转动功能配置和测试](TripleServoController.md)       | Done    | [舵机供电时没有共地无法正常运行(Done)](ErrorReport.md)<br/>[串口通信问题(Done)](TripleServoController.md#A)<br/>[电机响应问题(Done)](TripleServoController.md#A)                          |
| 3      | [Leap Motion手势控制数据处理](Leap-Motion手势控制数据处理.md) | Done    | [LeapMotion配置和测试(Done)](LeapMotion-Configration.md)<br/>[Leap Motion控制器未识别(Done)](LeapMotion-Configration.md)<br/>[SDK版本不兼容(Done)](LeapMotion-Configration.md) |
| 4      | [轨迹记录与输出程序开发](TrajectoryGeneration.md)        | Done    | [数据接收问题(Done)](TrajectoryGeneration.md#A)<br/>[视觉呈现问题(Done)](TrajectoryGeneration.md#A)                                                                        |
| 5      | [系统集成测试与调试](系统集成测试与调试.md)                     | Done    | [串口通信故障(Done)](TripleServoController.md#A)<br/>[PID参数调整(Done)](PID.md#A)<br/>[Leap Motion数据异常(Done)](Leap-Motion手势控制数据处理.md#A)                                 |


### 机械结构 Structure

| TaskID  | Description                            | Status   | Errors                   |
|---------|----------------------------------------|----------|--------------------------|
| 0       | 装置原型结构原理设计与制作                          | Done     | 原型制作时材料强度不足，导致结构承重问题     |
| 1       | Leap Motion传感器安装与调试                    | Done     | 传感器安装位置导致信号遮挡和误读         |
| 2       | 球体滚落收集装置的制作和调整                         | On Hold  | 收集装置的重置机制初期运行缓慢          |
| 3       | 最终装置的整体制作和结构调整                         | Done     | 最终装置在组装过程中发现部分接口不匹配      |
| 4       | 硬件组件的集成与调试                             | Done     | 硬件组件间的电源分配不均，导致部分模块电力不足  |

### 整体外观 Art

| TaskID   | Description      | Status   | Errors                  |
|----------|------------------|----------|-------------------------|
| 0        | 装置原型设计迭代         | Done     | 原型设计时外观效果设计不准确          |
| 1        | 材料选择和采购          | Done     | 材料采购中遇到供应链延迟问题          |
| 2        | 图像输出设计与实现        | Done     | 图像输出时色彩失真，需调整显示设备的色彩配置  |
| 3        | 装置外观设计与制作        | Done     | 外观设计在制作过程中发现部分设计不适合实际应用 |
| 4        | 展示视频的制作          | Done     | 视频拍摄过程中遇到灯光和背景搭配问题      |


