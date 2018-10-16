from .util import Vector

# This is my edit of the tripy lib. Changed to support my vectors, and some other additions. - qwerty

import math
TWO_PI = 2 * math.pi
PI = math.pi


def earclip(polygon):
    ear_vertex = []
    triangles = []
    polygon = [point.copy() for point in polygon]

    point_count = len(polygon)
    for i in range(point_count):
        prev_index = i - 1
        prev_point = polygon[prev_index]
        point = polygon[i]
        next_index = (i + 1) % point_count
        next_point = polygon[next_index]

        if is_ear(prev_point, point, next_point, polygon):
            ear_vertex.append(point)

    while ear_vertex and point_count >= 3:
        ear = ear_vertex.pop(0)
        i = polygon.index(ear)
        prev_index = i - 1
        prev_point = polygon[prev_index]
        next_index = (i + 1) % point_count
        next_point = polygon[next_index]

        polygon.remove(ear)
        point_count -= 1
        triangles.append([Vector(prev_point.x, prev_point.y), Vector(ear.x, ear.y), Vector(next_point.x, next_point.y)])
        if point_count > 3:
            prev_prev_point = polygon[prev_index - 1]
            next_next_index = (i + 1) % point_count
            next_next_point = polygon[next_next_index]

            groups = [
                (prev_prev_point, prev_point, next_point, polygon),
                (prev_point, next_point, next_next_point, polygon)
            ]
            for group in groups:
                p = group[1]
                if is_ear(*group):
                    if p not in ear_vertex:
                        ear_vertex.append(p)
                elif p in ear_vertex:
                    ear_vertex.remove(p)
    return triangles


def is_clockwise(polygon):
    s = 0
    polygon_count = len(polygon)
    for i in range(polygon_count):
        point = polygon[i]
        point2 = polygon[(i + 1) % polygon_count]
        s += (point2.x - point.x) * (point2.y + point.y)
    return s > 0


def is_convex(prev, point, next):
    return triangle_sum(prev.x, prev.y, point.x, point.y, next.x, next.y) < 0


def is_ear(p1, p2, p3, polygon):
    return contains_no_points(p1, p2, p3, polygon) and is_convex(p1, p2, p3) and triangle_area(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y) > 0


def contains_no_points(p1, p2, p3, polygon):
    for pn in polygon:
        if pn in (p1, p2, p3):
            continue
        elif is_point_inside(pn, p1, p2, p3):
            return False
    return True


def is_point_inside(p, a, b, c):
    return triangle_area(a.x, a.y, b.x, b.y, c.x, c.y) == sum([triangle_area(p.x, p.y, b.x, b.y, c.x, c.y), triangle_area(p.x, p.y, a.x, a.y, c.x, c.y), triangle_area(p.x, p.y, a.x, a.y, b.x, b.y)])


def triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


def triangle_sum(x1, y1, x2, y2, x3, y3):
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)


def is_convex_polygon(polygon):
    try:
        if len(polygon) < 3:
            return False

        old_x, old_y = polygon[-2]
        new_x, new_y = polygon[-1]
        new_direction = math.atan2(new_y - old_y, new_x - old_x)
        angle_sum = 0.0

        for ndx, newpoint in enumerate(polygon):
            old_x, old_y, old_direction = new_x, new_y, new_direction
            new_x, new_y = newpoint
            new_direction = math.atan2(new_y - old_y, new_x - old_x)
            if old_x == new_x and old_y == new_y:
                return False
            angle = new_direction - old_direction
            if angle <= -PI:
                angle += TWO_PI
            elif angle > PI:
                angle -= TWO_PI
            orientation = 1.0 if angle > 0.0 else -1.0
            if ndx == 0:
                if angle == 0.0:
                    return False
            else:
                if orientation * angle <= 0.0:
                    return False

            angle_sum += angle

        return abs(round(angle_sum / TWO_PI)) == 1
    except (ArithmeticError, TypeError, ValueError):
        return False
