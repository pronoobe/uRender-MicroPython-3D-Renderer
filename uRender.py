from GR import *  # Importing all from the GR module
from math import acos, sqrt, pi

# Function to convert degree angles to radians for x, y, z
def get_pos_vec(x, y, z):
    return list((x/180*pi, y/180*pi, z/180*pi))

class MicroRender:
    # Initialization of the MicroRender class
    def __init__(self, camera_pos=[0, 0, 0], rotation_angles=[0, 0, 0], screen_x=128, screen_y=64):
        self.renderer = GraphRender(camera_pos, rotation_angles)  # Creating a GraphRender object
        self.camera_pos = camera_pos
        self.rotation_angles = rotation_angles
        self.screen_x = screen_x  # Width of the screen
        self.screen_y = screen_y  # Height of the screen
        self.lines = []  # List to store lines

    # Method to render points and lines on the screen
    def rending(self, screen, points, line=False, show_index=False):
        try:
            screen.fill(0)  # Clearing the screen
            # Projecting 3D points onto a 2D plane
            projected_points_graph_render = self.renderer.project_points(points)
            # Scaling points to fit the screen
            show_points = self.renderer.scale_to_screen(self.screen_x, self.screen_y, projected_points_graph_render)

            # Drawing points and optionally their indices
            for point in show_points:
                screen.ellipse(int(point[0]), int(point[1]), 2, 2, 1, not line)
                if show_index:
                    screen.text(str(show_points.index(point) + 1), int(point[0]), int(point[1]))

            # Drawing lines if the line option is True
            if line:
                for point1i in range(len(show_points)):
                    for point2i in range(len(show_points)):
                        if (point1i + 1, point2i + 1) in self.lines:
                            point1 = show_points[point1i]
                            point2 = show_points[point2i]
                            x1, y1 = point1[0], point1[1]
                            x2, y2 = point2[0], point2[1]
                            screen.line(int(x1), int(y1), int(x2), int(y2), 1)
            screen.show()  # Displaying the rendered content
        except ValueError:
            print("error rending")

    # Method to set the camera position
    def set_camera_pos(self, camera_pos):
        self.renderer.camera_pos = Vector(camera_pos)

    # Method to set the camera rotation angle
    def set_camera_angle(self, rotation_angles):
        self.renderer.rotation_angles = rotation_angles
        self.renderer.rotation_matrix = self.renderer.create_rotation_matrix(rotation_angles)

    # Method to add a line between two points
   
