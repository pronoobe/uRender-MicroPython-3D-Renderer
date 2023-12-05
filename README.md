# uRender-MicroPython-3D-Renderer
# micropython 3D图形渲染库


## 简介
这个项目是一个为micropython微控制器编写的3D图形渲染库，使用ESP32进行测试。它允许用户在OLED显示屏上渲染简单的3D图形，包括点和线的渲染以及视角的调整。
## Introduction
This project is a 3D graphics rendering library for the micropython microcontroller, implemented in MicroPython. It allows users to render simple 3D graphics on an OLED display, including point and wireframe rendering, as well as camera viewpoint control.

## 功能
- **3D点渲染**：在三维空间中定义点，并将它们渲染到二维屏幕上。
- **线框渲染**：连接三维空间中的点以创建线框图形。
- **视角控制**：调整相机的位置和角度来查看三维图形。
- 渲染 3D 点和线条到屏幕。
- 支持正交和中心投影方式的渲染。
- 提供设置相机位置和旋转角度的功能。
- 允许定义点之间的连线。
## Features
- **3D Point Rendering**: Define points in three-dimensional space and render them on a two-dimensional screen.
- **Wireframe Rendering**: Connect points in three-dimensional space to create wireframe graphics.
- **Viewpoint Control**: Adjust the camera's position and angle to view 3D graphics.

- Renders 3D points and lines to the screen.

- Supports rendering with orthogonal and central projection methods.

- Offers functionality to set the camera position and rotation angles.

- Allows defining lines between points.
## 安装要求
- ESP32微控制器
- MicroPython固件
- SSD1306 OLED显示屏
- 必要的MicroPython库，如`ssd1306`
## Requirements
- ESP32 microcontroller
- MicroPython firmware
- SSD1306 OLED display
- Necessary MicroPython libraries, such as `ssd1306`

## 安装指南
1. 确保ESP32微控制器已刷入MicroPython固件。
2. 将本项目的文件下载到ESP32上。
3. 通过MicroPython的包管理器安装所需库。
4. `ssd1306`模块源自开源项目[stlehmann/micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py)，请确保遵循其许可证规定。
## Installation Guide
1. Ensure that the ESP32 microcontroller is loaded with MicroPython firmware.
2. Download the files of this project to the ESP32.
3. Install required libraries via MicroPython's package manager.
4. The `ssd1306` module is sourced from the open-source project [stlehmann/micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py), ensure compliance with its license terms.

## 使用示例
以下是一个使用本库在ESP32上渲染3D图形的示例（具体可以参考test_main,py）：
## Usage Example
Below is an example of using this library to render 3D graphics on the ESP32:

```python
from ssd1306 import SSD1306_I2C
from machine import I2C
from uRender import MicroRender

# 初始化OLED显示屏
# Initialize the OLED display
oled = SSD1306_I2C(128, 64, I2C(1)) #I2C1 SCL=25 SDA=26

# 定义一些三维点
# Define some 3D points
points = [(10, 10, 10), (10, 10, 20), ...]

# Initialize the renderer
# 初始化渲染器
render = MicroRender(camera_pos=[3, -1, 0], rotation_angles=[0, 0, 0])

# 添加线条
# Add lines
render.add_line(1, 2)
render.add_line(1, 4)
render.add_line(1, 2)
render.add_line(1, 4)
render.add_line(2, 3)
render.add_line(3, 4)
render.add_line(4, 5)
render.add_line(5, 1)
render.add_line(5, 2)
render.add_line(5, 3)

# 渲染到OLED显示屏上
# Render to the OLED display
render.rending(oled, points, line=True, show_index=False)
```
# 贡献
欢迎对本项目进行改进！如有建议或发现bug，请提交issue或pull request。
# Contributions
Contributions to improve this project are welcome! If you have suggestions or find bugs, please submit an issue or pull request.
# 许可
本项目采用MIT许可证。同时，使用的ssd1306模块遵循其原项目stlehmann/micropython-ssd1306的许可规定。
# License
This project is licensed under the MIT License. Additionally, the ssd1306 module used adheres to the licensing terms of its original project stlehmann/micropython-ssd1306.
