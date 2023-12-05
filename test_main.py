from ssd1306 import *
from machine import I2C, Timer, Pin
import time
from uRender import *
from math import sin, cos

# Initialize an OLED display using the I2C protocol
oled = SSD1306_I2C(128, 64, I2C(1))

# Define a set of 3D points to create a model
points = [
    (10, 10, 0), (10, -10, 0), (-10, -10, 0), (-10, 10, 0),
    (10, 10, 7), (10, -10, 7), (-10, -10, 7), (-10, 10, 7),
    (0, 0, 12),
]

# Initialize a renderer for 3D graphics
render = MicroRender(camera_pos=[3, -1, 0], rotation_angles=[0, 0, 0], screen_x=128, screen_y=64)

# Add lines to define the edges of the 3D model
render.add_line(1, 2)
render.add_line(2, 3)
render.add_line(3, 4)
render.add_line(4, 1)
render.add_line(1, 5)
render.add_line(2, 6)
render.add_line(3, 7)
render.add_line(4, 8)
render.add_line(5, 6)
render.add_line(6, 7)
render.add_line(7, 8)
render.add_line(5, 8)
render.add_line(5, 9)
render.add_line(6, 9)
render.add_line(7, 9)
render.add_line(9, 8)

# Change the camera position for different perspectives
render.set_camera_pos([15, 15, 15])

# Render the model from various angles
for angle in range(0, 36):
    ang = get_pos_vec(angle // 10, angle // 10, angle)
    render.set_camera_angle(ang)
    render.rending_center(oled, points, line=1, show_index=0)

# Set a normal vector for rendering
normal_vec = [0, 1, 1]

# Rotate and render the model for a full 360-degree rotation
for angle in range(0, 360):
    rotated_points = rotate_points(points, (0, angle, 0))
    render.rending_ord(oled, rotated_points, normal_vec, line=1, show_index=0)

