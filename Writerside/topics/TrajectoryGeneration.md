# TrajectoryGeneration 数据生成轨迹功能配置和测试

## 概述
本指南旨在介绍如何配置和测试`TrajectoryGeneration`功能，这是一个基于TouchDesigner开发的测试程序，用于实时监测、记录并展示对象（如小球）的运动轨迹。

## 环境要求
- 安装TouchDesigner
- 准备外部数据发送设备（例如配备摄像头的计算机）
- OSC协议支持

## 配置步骤
1. **数据发送源准备**：确保外部设备（如摄像头）已设置好，能够通过OSC协议发送数据。
2. **启动TouchDesigner**：打开TouchDesigner并加载`TrajectoryGeneration.toe`文件。
3. **配置OSC接收**：在TouchDesigner中配置OSC In DAT节点，以确保正确接收来自外部设备的数据。
4. **小球动态位置控制**：根据接收到的数据，程序会在TouchDesigner内动态控制小球的位置。

## 正常运行的预期结果
- 外部数据实时接收：通过OSC协议，程序实时接收外部数据。
- 小球位置实时更新：根据接收到的数据，小球在TouchDesigner界面中的位置应实时变化。
- 运动轨迹的生成和展示：程序应自动记录并在界面上实时展示小球的运动轨迹。
- 视觉效果呈现：程序应根据实时数据生成吸引人的视觉效果。

<video src="Visual-Identification1.mp4" preview-src="Visual-Identification2.jpg"/>

## 故障排除
- **数据接收问题**：如果无法接收数据，请检查OSC In DAT节点的配置，确保其端口和地址模式与数据发送设备相匹配。
- **数据延迟或丢失**：检查网络连接是否稳定，并确认发送设备的配置是否正确。
- **视觉效果不符合预期**：检查Geo COMP、Trail SOP和Render TOP的设置，确保它们正确响应接收到的数据。