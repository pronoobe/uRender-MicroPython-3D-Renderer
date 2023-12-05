from math import pi, sin, cos

class Vector:
    def __init__(self, data):
        self.data = data

    def __add__(self, other):
        return Vector([x + y for x, y in zip(self.data, other.data)])

    def __sub__(self, other):
        return Vector([x - y for x, y in zip(self.data, other.data)])

    def __mul__(self, other):
        if isinstance(other, Vector):
            # Cross product
            return Vector([
                self.data[1] * other.data[2] - self.data[2] * other.data[1],
                self.data[2] * other.data[0] - self.data[0] * other.data[2],
                self.data[0] * other.data[1] - self.data[1] * other.data[0]
            ])
        else:
            # Scalar multiplication
            return Vector([x * other for x in self.data])

    def norm(self):
        return sum(x ** 2 for x in self.data) ** 0.5

    def normalize(self):
        norm = self.norm()
        return Vector([x / norm for x in self.data])


class Matrix:
    def __init__(self, data):
        self.data = data

    def __mul__(self, other):
        # Multiplying with Vector or Matrix
        if isinstance(other, Vector):
            other_data = [[x] for x in other.data]
        else:
            other_data = other.data

        result = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(other_data[0])):
                row.append(sum(self.data[i][k] * other_data[k][j] for k in range(len(other_data))))
            result.append(row)

        # Return result as Vector or Matrix
        if isinstance(other, Vector):
            return Vector([x[0] for x in result])
        return Matrix(result)

def rotate_points(points, angles):
    # Calculate centroid of points
    centroid = Vector([0, 0, 0])
    for point in points:
        if not isinstance(point, Vector):
            point = Vector(point)
        centroid = centroid + point
    centroid = centroid * (1 / len(points))

    # Convert angles to radians
    angle_x, angle_y, angle_z = [angle * pi / 180 for angle in angles]

    # Create rotation matrices
    rot_x = Matrix([[1, 0, 0], [0, cos(angle_x), -sin(angle_x)], [0, sin(angle_x), cos(angle_x)]])
    rot_y = Matrix([[cos(angle_y), 0, sin(angle_y)], [0, 1, 0], [-sin(angle_y), 0, cos(angle_y)]])
    rot_z = Matrix([[cos(angle_z), -sin(angle_z), 0], [sin(angle_z), cos(angle_z), 0], [0, 0, 1]])
    rotation_matrix = rot_z * rot_y * rot_x

    # Rotate points and return
    rotated_points = []
    for point in points:
        rotated_point = rotation_matrix * (point - centroid) + centroid
        rotated_points.append(rotated_point)
    return rotated_points

class GraphRender_Ord:
    def __init__(self, normal_vector):
        self.normal = Vector(normal_vector)

    def dot_product(self, v1, v2):
        return sum(x * y for x, y in zip(v1.data, v2.data))

    def change_normal(self, normal_vector):
        self.normal = Vector(normal_vector)

    def project_point(self, point):
        if not isinstance(point, Vector):
            point = Vector(point)
        normal_normalized = self.normal.normalize()
        return point - normal_normalized * self.dot_product(point, normal_normalized)

    def orthogonal_projection(self, points):
        return [self.project_point(point) for point in points]

class GraphRender:
    def __init__(self, camera_pos, rotation_angles):
        self.camera_pos = Vector(camera_pos)
        self.rotation_angles = rotation_angles
        self.rotation_matrix = self.create_rotation_matrix(rotation_angles)
        self.ord_render = GraphRender_Ord(Vector([0, 0, 1]))

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

        return R_z * R_y * R_x

    def project_points_ord(self, points, normal_vector):
        self.ord_render.normal = Vector(normal_vector)
        projected_points = self.ord_render.orthogonal_projection(points)
        projected_points_data = [p.data for p in projected_points]
        return projected_points_data

    def project_points_center(self, points):
        projected_points = []
        for point in points:
            transformed_point = self.rotation_matrix * (Vector(point) - self.camera_pos)
            if transformed_point.data[2] != 0:
                projected_point = [transformed_point.data[0] / transformed_point.data[2],
                                   transformed_point.data[1] / transformed_point.data[2]]
            else:
                projected_point = [float('inf'), float('inf')]

            projected_points.append(projected_point)
        return projected_points

    @staticmethod
    def scale_to_screen(screen_width, screen_height, points):
        screen_width, screen_height = screen_width * 0.9, screen_height * 0.9
        min_x, max_x = min(point[0] for point in points), max(point[0] for point in points)
        min_y, max_y = min(point[1] for point in points), max(point[1] for point in points)
        scale_x, scale_y = (screen_width / (max_x - min_x), screen_height / (max_y - min_y)) if (max_x - min_x) != 0 else (1, 1)
        scale = min(scale_x, scale_y)
        scaled_points = [[(point[0] - min_x) * scale, (point[1] - min_y) * scale] for point in points]
        center_x, center_y = sum(point[0] for point in scaled_points) / len(scaled_points), sum(point[1] for point in scaled_points) / len(scaled_points)
        screen_center_x, screen_center_y = screen_width / 2, screen_height / 2
        shift_x, shift_y = screen_center_x - center_x, screen_center_y - center_y
        final_points = [[max(0, min(screen_width - 1, int(round(point[0])))) + 3,
                         max(0, min(screen_height - 1, int(round(point[1])))) + 3] for point in scaled_points]
        return final_points

