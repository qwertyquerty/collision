import math
from numbers import Real
from typing import Any, Union


LEFT_VORONOI_REGION = -1
MIDDLE_VORONOI_REGION = 0
RIGHT_VORONOI_REGION = 1
ALLOWED_NUM_TYPES = (int, float)


class Vector:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other: Any):
        if isinstance(other, ALLOWED_NUM_TYPES):
            return Vector(self.x+other, self.y+other)

        return Vector(self.x+other.x, self.y+other.y)

    def __mul__(self, other: Any):
        if isinstance(other, ALLOWED_NUM_TYPES):
            return Vector(self.x*other, self.y*other)

        return Vector(self.x*other.x, self.y*other.y)

    def __sub__(self, other: Any):
        if isinstance(other, ALLOWED_NUM_TYPES):
            return Vector(self.x-other, self.y-other)

        return Vector(self.x-other.x, self.y-other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __truediv__(self, other: Any):
        if isinstance(other, ALLOWED_NUM_TYPES):
            return Vector(self.x/other, self.y/other)

        return Vector(self.x/other.x, self.y/other.y)

    def __floordiv__(self, other: Any):
        if isinstance(other, ALLOWED_NUM_TYPES):
            return Vector(self.x//other, self.y//other)

        return Vector(self.x//other.x, self.y//other.y)

    def __mod__(self, other: Any):
        if isinstance(other, ALLOWED_NUM_TYPES):
            return Vector(self.x % other, self.y % other)

        return Vector(self.x % other.x, self.y % other.y)

    def __eq__(self, other: Any):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Any):
        if not isinstance(other, Vector):
            return True

        return self.x != other.x or self.y != other.y

    def __getitem__(self, index: int):
        return [self.x, self.y][index]

    def __contains__(self, value):
        return value == self.x or value == self.y

    def __len__(self):
        return 2

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Vector [{x}, {y}]".format(x=self.x, y=self.y)

    def copy(self):
        return Vector(self.x, self.y)

    def set(self, other):
        self.x = other.x
        self.y = other.y

    def perp(self):
        return Vector(self.y, -self.x)

    def rotate(self, angle: Union[int, float, Real]):
        return Vector(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))

    def reverse(self):
        return Vector(-self.x, -self.y)

    def int(self):
        return Vector(int(self.x), int(self.y))

    def normalize(self):
        dot = self.ln()
        return self / dot

    def project(self, other):
        amt = self.dot(other) / other.ln2()

        return Vector(amt * other.x,  amt * other.y)

    def project_n(self, other):
        amt = self.dot(other)

        return Vector(amt * other.x, amt * other.y)

    def reflect(self, axis):
        v = Vector(self.x, self.y)
        v = v.project(axis) * 2
        v = -v

        return v

    def reflect_n(self, axis):
        v = Vector(self.x, self.y)
        v = v.project_n(axis) * 2
        v = -v

        return v

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def ln2(self):
        return self.dot(self)

    def ln(self):
        return math.sqrt(self.ln2())


def flatten_points_on(points, normal, result):
    minpoint = math.inf
    maxpoint = -math.inf

    for i in range(len(points)):
        dot = points[i].dot(normal)
        if dot < minpoint:
            minpoint = dot
        if dot > maxpoint:
            maxpoint = dot

    result[0] = minpoint
    result[1] = maxpoint


def is_separating_axis(a_pos, b_pos, a_points, b_points, axis, response=None):
    range_a = [0, 0]
    range_b = [0, 0]

    offset_v = b_pos-a_pos

    projected_offset = offset_v.dot(axis)

    flatten_points_on(a_points, axis, range_a)
    flatten_points_on(b_points, axis, range_b)

    range_b[0] += projected_offset
    range_b[1] += projected_offset

    if range_a[0] > range_b[1] or range_b[0] > range_a[1]:
        return True

    if response:

        overlap = 0

        if range_a[0] < range_b[0]:
            response.a_in_b = False

            if range_a[1] < range_b[1]:
                response.b_in_a = False

            else:
                option_1 = range_a[1] - range_b[1]
                option_2 = range_b[1] - range_a[1]
                overlap = option_1 if option_1 < option_2 else option_2

        else:
            response.b_in_a = False

            if range_a[1] > range_b[1]:
                overlap = range_a[0] - range_b[1]
                response.a_in_b = False

            else:
                option_1 = range_a[1] - range_b[0]
                option_2 = range_b[1] - range_a[0]

                overlap = option_1 if option_1 < option_2 else option_2

        abs_overlap = abs(overlap)
        if abs_overlap < response.overlap:
            response.overlap = abs_overlap
            response.overlap_n.set(axis)
            if overlap < 0:
                response.overlap_n = response.overlap_n.reverse()

    return False


def voronoi_region(line, point):
    dp = point.dot(line)

    if dp < 0:
        return LEFT_VORONOI_REGION
    elif dp > line.ln2():
        return RIGHT_VORONOI_REGION
    return MIDDLE_VORONOI_REGION
