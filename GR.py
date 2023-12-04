from math import pi, sin, cos

class Vector:
    # Vector class initialization
    def __init__(self, data):
        self.data = data  # Stores the vector data

    # Overloading the addition operator for vector addition
    def __add__(self, other):
        return Vector([x + y for x, y in zip(self.data, other.data)])

    # Overloading the subtraction operator for vector subtraction
    def __sub__(self, other):
        return Vector([x - y for x, y in zip(self.data, other.data)])

    # Overloading the multiplication operator
    def __mul__(self, other):
        if isinstance(other, Vector):
            # Cross product for vector multiplication
            return Vector([
                self.data[1] * other.data[2] - self.data[2] * other.data[1],
                self.data[2] * other.data[0] - self.data[0] * other.data[2],
                self.data[0] * other.data[1] - self.data[1] * other.data[0]
            ])
        else:
            # Scalar multiplication
            return Vector([x * other for x in self.data])

    # Calculate the Euclidean norm (magnitude) of the vector
    def norm(self):
        return sum(x ** 2 for x in self.data) ** 0.5

    # Normalize the vector (make its magnitude 1)
    def normalize(self):
        norm = self.norm()
        return Vector([x / norm for x in self.data])


class Matrix:
    # Matrix class initialization
    def __init__(self, data):
        self.data = data  # Stores the matrix data

    # Overloading the multiplication operator for matrix multiplication
    def __mul__(self, other):
        # Check if multiplying with a Vector
        if isinstance(other, Vector):
            # Treat Vector as a column matrix for multiplication
            other_data = [[x] for x in other.data]
        else:
            other_data = other.data

        result = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(other_data[0])):
                row.append(sum(self.data[i][k] * other_data[k][j] for k in range(len(other_data))))
            result.append(row)

        # If multiplying with a Vector, return a Vector
        if isinstance(other, Vector):
            return Vector([x[0] for x in result])
        return Matrix(result)


class GraphRender:
    # Graph rendering class initialization
    def __init__(self, camera_pos, rotation_angles):
        self.camera_pos = Vector(camera_pos)
        self.rotation_angles = rotation_angles
        self.rotation_matrix = self.create_rotation_matrix(rotation_angles)

    # Creates a rotation matrix based on given angles
    def create_rotation_matrix(self, angles):
        R_x = Matrix([
            [1, 0, 0],
            [0, cos(angles[0]), -sin(angles[0])],
            [0, sin(angles[0]), cos(angles[0])]
        ])

        R_y = Matrix([
            [cos(angles[1]), 0, sin(angles[1])],
            [0, 1, 0],
            [-sin(angles[1]), 0, cos(angles[1])]
        ])

        R_z = Matrix([
            [cos(angles[2]), -sin(angles[2]), 0],
            [sin(angles[2]), cos(angles[2]), 0],
            [0, 0, 1]
        ])

        # Combining the rotation matrices
        return R_z * R_y * R_x

    # Projects 3D points onto a 2D plane
    def project_points(self, points):
        projected_points = []
        for point in points:
            # Apply rotation and translate relative to camera position
            transformed_point = self.rotation_matrix * (Vector(point) - self.camera_pos)

            # Apply perspective projection
            if transformed_point.data[2] != 0:
                projected_point = [transformed_point.data[0] / transformed_point.data[2],
                                   transformed_point.data[1] / transformed_point.data[2]]
            else:
                projected_point = [float('inf'), float('inf')]

            projected_points.append(projected_point)

        return projected_points

    # Static method to scale and center points to fit within the screen dimensions
    @staticmethod
    def scale_to_screen(screen_width, screen_height, points: list):
        screen_width, screen_height = screen_width * 0.9, screen_height * 0.9
        # Find the range of point coordinates
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)

        # Calculate scaling factors
        if (max_x - min_x) != 0:
            scale_x = screen_width / (max_x - min_x)
            scale_y = screen_height / (max_y - min_y)
        else:
            scale_x, scale_y = 1, 1
        scale = min(scale_x, scale_y)

        # Scale and translate the points
        scaled_points = [[(point[0] - min_x) * scale, (point[1] - min_y) * scale] for point in points]

        # Calculate the center of the scaled points
        center_x = sum(point[0] for point in scaled_points) / len(scaled_points)
        center_y = sum(point[1] for point in scaled_points) / len(scaled_points)

        # Calculate the shift required to center the points on the screen
        screen_center_x, screen_center_y = screen_width / 2, screen_height / 2
        shift_x, shift_y = screen_center_x - center_x, screen_center_y - center_y
        centered_points = [[point[0] + shift_x, point[1] + shift_y] for point in scaled_points]

        # Adjust points to be within screen boundaries and apply a final shift
        final_points = [[max(0, min(screen_width - 1, int(round(point[0])))) + 3,
                         max(0, min(screen_height - 1, int(round(point[1])))) + 3] for point in centered_points]
        return final_points
