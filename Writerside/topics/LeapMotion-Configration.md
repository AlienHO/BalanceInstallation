# LeapMotion配置和测试指南

## 概述

本指南提供配置Leap Motion控制器和运行Python测试程序 testLEAP.py 的步骤。

## 环境要求

- LeapMotion控制器(LeapMotion一代)
- Windows, macOS, 或 Linux操作系统
- Python版本：2.7.x、3.6.x、>=3.7,<3.8.0a0 或 >=3.8,<3.9.0a0

## 步骤


### 1. 安装Leap Motion驱动程序

1. **下载驱动程序**：从[TechSpot](https://www.techspot.com/downloads/6701-leap-motion.html)下载Leap Motion 2.3.1驱动。

2. **安装驱动程序**：根据安装向导完成驱动安装。

3. **设备校准**：在Leap Motion控制面板中选择 "重新校准设备"。 在该界面直接重启电脑激活Leap Motion。

4. **检查状态**： 重启后，确保状态栏中的Leap Motion图标显示绿灯。


### 2. 安装Anaconda

1. **下载**：访问[Anaconda官方网站](https://www.anaconda.com/products/individual)下载Anaconda。
2. **安装**：运行安装程序并遵循安装指南。

### 3. 配置Python环境

1. **打开终端**：启动命令行界面。
2. **创建环境**：运行以下命令创建一个新的Python环境（例如，使用Python 3.7）：

   ```bash
   conda create -n leap_env python=3.7
   ```
3. **激活环境**：

   ```bash
   conda activate leap_env
   ```

### 4. 安装Leap Motion SDK

1. **安装SDK**：在激活的环境中，运行以下命令安装Leap Motion SDK：

   ```bash
   conda install -c speleo3 leap-motion-python
   ```

### 5. 其他依赖项

如果程序运行需要其他库（如 `numpy`、`opencv` 等），请在同一环境中安装这些依赖项。

### 6. 运行测试程序

1. **下载**：将 `testLEAP.py` 文件保存到计算机。
2. **运行**：在激活了 `leap_env` 的终端中，导航到脚本所在的文件夹，并使用以下命令运行脚本：

   ```bash
   python testLEAP.py
   ```

## 故障排除

- 确保Leap Motion控制器被正确识别。
- 如遇Leap Motion SDK问题，检查Python版本兼容性。
- 运行脚本错误时，确认所有依赖库已安装。

## 配置参考

[Leap Motion SDK (Python modules only)leap-motion-python `2.3.1+31549`](https://anaconda.org/speleo3/leap-motion-python)
