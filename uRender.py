from GR import *
from math import acos, sqrt, pi

# Function to convert angles from degrees to radians
def get_pos_vec(x, y, z):
    return list((x / 180 * pi, y / 180 * pi, z / 180 * pi))

class MicroRender:
    def __init__(self, camera_pos=[0, 0, 0], rotation_angles=[0, 0, 0], screen_x=128, screen_y=64):
        # Initialize the renderer with camera position, rotation angles, and screen dimensions
        self.renderer = GraphRender(camera_pos, rotation_angles)
        self.camera_pos = camera_pos
        self.rotation_angles = rotation_angles
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.lines = []

    # Method to render points using orthogonal projection
    def rending_ord(self, screen, points, normal_vec, line=False, show_index=False):
        try:
            screen.fill(0)
            projected_points = self.renderer.project_points_ord(points, normal_vec)
            display_points = self.renderer.scale_to_screen(self.screen_x, self.screen_y, projected_points)

            # Display points and optionally their indices
            for point in display_points:
                screen.ellipse(int(point[0]), int(point[1]), 2, 2, 1, not line)
                if show_index:
                    screen.text(str(display_points.index(point) + 1), int(point[0]), int(point[1]))

            # Draw lines between points if specified
            if line:
                for i in range(len(display_points)):
                    for j in range(len(display_points)):
                        if (i + 1, j + 1) in self.lines:
                            x1, y1 = display_points[i][0], display_points[i][1]
                            x2, y2 = display_points[j][0], display_points[j][1]
                            screen.line(int(x1), int(y1), int(x2), int(y2), 1)
            screen.show()
        except ValueError:
            print("error rendering")

    # Method to render points using central projection
    def rending_center(self, screen, points, line=False, show_index=False):
        try:
            screen.fill(0)
            projected_points = self.renderer.project_points_center(points)
            display_points = self.renderer.scale_to_screen(self.screen_x, self.screen_y, projected_points)

            # Similar rendering logic as in rending_ord
            for point in display_points:
                screen.ellipse(int(point[0]), int(point[1]), 2, 2, 1, not line)
                if show_index:
                    screen.text(str(display_points.index(point) + 1), int(point[0]), int(point[1]))

            if line:
                for i in range(len(display_points)):
                    for j in range(len(display_points)):
                        if (i + 1, j + 1) in self.lines:
                            x1, y1 = display_points[i][0], display_points[i][1]
                            x2, y2 = display_points[j][0], display_points[j][1]
                            screen.line(int(x1), int(y1), int(x2), int(y2), 1)
            screen.show()
        except ValueError:
            print("error rendering")

    # Method to set the camera position
    def set_camera_pos(self, camera_pos):
        self.renderer.camera_pos = Vector(camera_pos)

    # Method to set the camera rotation angle
    def set_camera_angle(self, rotation_angles):
        self.renderer.rotation_angles = rotation_angles
        self.renderer.rotation_matrix = self.renderer.create_rotation_matrix(rotation_angles)

    # Method to define lines between points
    def add_line(self, p1, p2):
        self.lines.append((p1, p2))

