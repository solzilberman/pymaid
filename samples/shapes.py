from typing import List, Tuple
import math

class Point3D:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

class Shape3D:
    def __init__(self, points: List[Point3D]) -> None:
        self.points = points

    def calculate_area(self) -> float:
        raise NotImplementedError

class Triangle(Shape3D):
    def __init__(self, points: List[Point3D]) -> None:
        super().__init__(points)

    def calculate_area(self) -> float:
        a = self.points[0].distance(self.points[1])
        b = self.points[1].distance(self.points[2])
        c = self.points[2].distance(self.points[0])
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

class Quadrilateral(Shape3D):
    def __init__(self, points: List[Point3D]) -> None:
        super().__init__(points)

    def calculate_area(self) -> float:
        x_coords = [point.x for point in self.points]
        y_coords = [point.y for point in self.points]
        return 0.5 * abs(sum(x_coords[i] * y_coords[i + 1] - x_coords[i + 1] * y_coords[i] for i in range(len(self.points) - 1)) + x_coords[-1] * y_coords[0] - y_coords[-1] * x_coords[0])

class Line3D:
    def __init__(self, start: Point3D, end: Point3D) -> None:
        self.start = start
        self.end = end

    def length(self) -> float:
        return self.start.distance(self.end)

class Polyline(Line3D):
    def __init__(self, points: List[Point3D]) -> None:
        self.points = points

    def length(self) -> float:
        return sum(self.points[i].distance(self.points[i + 1]) for i in range(len(self.points) - 1))

class BezierCurve(Line3D):
    def __init__(self, control_points: List[Point3D]) -> None:
        self.control_points = control_points