from ssd1306 import *  # Importing the ssd1306 module
from machine import I2C, Timer, Pin  # Importing necessary classes from machine module
import time
from uRender import *  # Importing everything from the uRender module

from math import sin, cos

# Creating an instance of the SSD1306_I2C class for OLED display
oled = SSD1306_I2C(128, 64, I2C(1))

# Defining a list of 3D points
points = [
    (10, 10, 10),
    (10, 10, 20),
    (10, 5, 20),
    (15, 5, 20),
    (15, -15, -20),
]

# Initializing the MicroRender class with specific camera position, rotation angles, and screen dimensions
render = MicroRender(camera_pos=[3, -1, 0],
                     rotation_angles=[0, 0, 0],
                     screen_x=128,
                     screen_y=64)

# Adding lines between specified points
render.add_line(1, 2)
render.add_line(1, 4)
render.add_line(2, 3)
render.add_line(3, 4)
render.add_line(4, 5)
render.add_line(5, 1)
render.add_line(5, 2)
render.add_line(5, 3)

# Looping through angles to create a rotating effect
for angle in range(0, 360):
    # Converting angle to radians for x, y, z directions
    ang = get_pos_vec(angle//10, angle//10, angle)
    # Setting the camera's rotation angle
    render.set_camera_angle(ang)
    # Setting the camera's position
    render.set_camera_pos([1, 2, 0])
    # Rendering the points and lines onto the OLED display
    render.rending(oled, points, line=1, show_index=0)
