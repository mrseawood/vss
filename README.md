# 视频场景分割工具

这是一个基于PySceneDetect的视频场景分割工具，提供了友好的图形用户界面，可以帮助用户轻松地将视频文件按场景进行切割。

## 功能特点

- 图形用户界面，操作简单直观
- 支持多种视频格式（MP4, AVI, MKV, MOV, FLV, WMV）
- 实时进度显示和日志输出
- 批量处理多个视频文件
- 自动创建输出文件夹

## 安装要求

### Python版本
- Python 3.6 或更高版本

### 必需的Python库
1. PySceneDetect
   ```bash
   pip install scenedetect
   ```

2. 其他依赖项（已包含在Python标准库中）：
   - tkinter（GUI界面）
   - os（文件操作）
   - subprocess（进程管理）
   - threading（多线程支持）
   - locale（系统编码支持）

## 快速开始

1. 安装所有必需的依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行程序：
   ```bash
   python 使用PySceneDetect对视频进行场景切割-有GUI界面.py
   ```

## 使用说明

1. 启动程序后，您将看到一个带有使用说明的图形界面。

2. 使用步骤：
   - 点击"选择导入文件夹"按钮，选择包含视频文件的文件夹
   - 点击"选择导出文件夹"按钮，选择切割后视频片段的保存位置
   - 点击"开始切割"按钮，开始处理视频

注意事项：
- 支持的视频格式：MP4, AVI, MKV, MOV, FLV, WMV
- 每个视频将在输出文件夹中创建同名子文件夹存放切割片段
- 处理过程中请勿关闭程序

## 技术细节

### PySceneDetect 工作原理
PySceneDetect 通过分析视频帧之间的内容变化来检测场景切换。当相邻帧之间的差异超过特定阈值时，会被识别为一个新场景的开始。

### 系统要求
- 操作系统：Windows、macOS 或 Linux
- 磁盘空间：视频处理需要足够的存储空间，建议至少有处理视频大小两倍的可用空间

## 常见问题

### Q: 为什么我的视频没有被正确切割？
A: 可能的原因包括：
- 视频格式不受支持
- 视频文件损坏
- PySceneDetect 无法检测到明显的场景变化

### Q: 程序运行时出现错误提示
A: 请确保：
- 已正确安装所有依赖
- 视频文件可以正常播放
- 有足够的磁盘空间

## 技术支持

如果您在使用过程中遇到任何问题，请访问我们的网站：https://jmlovestore.com 获取支持。

## 许可证

本软件遵循 MIT 许可证发布。![123](https://github.com/user-attachments/assets/b94ef6fb-ac15-4a2a-aa15-10abb4a42c9f)
