# 轨迹记录与输出程序开发

## 文档介绍
- **目的**：介绍 `TrajectoryGeneration` 功能的配置和测试过程。
- **范围**：涵盖环境设置、配置步骤、正常运行预期结果和故障排除。

## 项目概述
`TrajectoryGeneration` 是一个基于TouchDesigner的测试程序，旨在实时监测、记录并展示对象（如小球）的运动轨迹。

### 环境要求
- 已安装TouchDesigner。
- 准备好的外部数据发送设备（例如配备摄像头的计算机）。
- 支持OSC协议的设备。

### 测试用例
1. **数据发送源准备**：配置外部设备以通过OSC协议发送数据。
2. **启动TouchDesigner**：加载 `TrajectoryGeneration.toe` 文件。
3. **配置OSC接收**：在TouchDesigner中设置OSC In DAT节点，确保接收外部设备数据。
4. **小球动态位置控制**：利用接收到的数据，在TouchDesigner内动态控制小球位置。

### 测试环境要求
- 确保TouchDesigner正确安装和配置。
- 验证外部设备和OSC协议的功能和连接。

## 正常运行的预期结果
- **外部数据实时接收**：程序通过OSC实时接收外部数据。
- **小球位置实时更新**：TouchDesigner中小球位置根据数据实时变化。
- **运动轨迹生成和展示**：程序记录并展示小球运动轨迹。
- **视觉效果呈现**：基于实时数据生成视觉效果。
<video src="Visual-Identification1.mp4" preview-src="Visual-Identification2.jpg"/>


## 故障排除
- **数据接收问题**：检查TouchDesigner中OSC In DAT节点配置是否正确。
- **数据延迟或丢失**：检查网络连接稳定性和发送设备配置。
- **视觉效果问题**：核实Geo COMP、Trail SOP和Render TOP的设置以响应数据。

{: id="A"}