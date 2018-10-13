from .util import vec, flatten_points_on, voronoi_region, is_separating_axis
from .poly import Poly
from .box import Box
from .circle import Circle
from .response import Response

import math

LEFT_VORONOI_REGION = -1
MIDDLE_VORONOI_REGION = 0
RIGHT_VORONOI_REGION  = 1
RESPONSE = Response()
TEST_POINT = Box(vec(0,0), 0.000001, 0.000001).to_poly()

def point_in_circle(p, c):
    difference_v = p - c.pos

    radius_sq = c.radius * c.radius

    distance_sq = difference_v.ln2()

    return distance_sq <= radius_sq

def point_in_polygon(p, poly):
    TEST_POINT.pos = p.copy()
    RESPONSE.clear()

    result = test_poly_poly(TEST_POINT, poly, RESPONSE)

    if result:
        return RESPONSE.a_in_b

    return result

def test_circle_circle(a, b, response = None):

    difference_v = b.pos - a.pos

    total_radius = a.radius + b.radius

    total_radius_sq = total_radius * total_radius

    distance_sq = difference_v.ln2()

    if distance_sq > total_radius_sq:
        return False

    if response:
        dist = math.sqrt(distance_sq)
        response.a = a
        response.b = b
        response.overlap = total_radius - dist
        response.overlap_n = difference_v.normalize()
        response.overlap_v = difference_v * response.overlap
        response.a_in_b = a.radius <= b.radius and dist <= b.radius - a.radius
        response.b_in_a = b.radius <= a.radius and dist <= a.radius - b.radius

    return True

def test_poly_circle(polygon, circle, response = None):
    circle_pos = circle.pos - polygon.pos
    radius = circle.radius
    radius2 = radius * radius
    points = polygon.points
    ln = len(points)

    for i in range(ln):
        next = 0 if i == ln - 1 else i + 1
        prev = ln - 1 if i == 0 else i - 1

        overlap = 0
        overlap_n = None

        edge = polygon.edges[i].copy()
        point = circle_pos - points[i]

        if response and point.ln2() > radius2:
            response.a_in_b = False

        region = voronoi_region(edge,point)

        if region == LEFT_VORONOI_REGION:
            edge = polygon.edges[prev].copy()

            point2 = circle_pos - points[prev]

            region = voronoi_region(edge, point2)

            if region == RIGHT_VORONOI_REGION:

                dist = point.ln()

                if dist > radius:
                    return False

                elif response:
                    response.b_in_a = False
                    overlap_n = point.normalize()
                    overlap = radius - dist


        elif region == RIGHT_VORONOI_REGION:

            edge = polygon.edges[next].copy()
            point = circle_pos - points[next]
            region = voronoi_region(edge,point)

            if region == LEFT_VORONOI_REGION:
                dist = point.ln()

                if dist > radius:
                    return False

                elif response:
                    response.b_in_a = False
                    overlap_n = point.normalize()
                    overlap = radius - dist

        else:

            normal = edge.perp().normalize()


            dist = point.dot(normal)

            dist_abs = abs(dist)

            if dist > 0 and dist_abs > radius:
                return False


            elif response:
                overlap_n = normal
                overlap = radius - dist

                if dist >= 0 or overlap < 2 * radius:
                    response.b_in_a = False

        if overlap_n and response and abs(overlap) < abs(response.overlap):
            response.overlap = overlap
            response.overlap_n = overlap_n.copy()

    if response:
        response.a = polygon
        response.b = circle
        reponse.overlap_v = response.overlap_n * response.overlap

    return True

def test_circle_poly(circle,polgon,response=None):
    result = test_poly_circle(polygon, circle, response)

    if result and response:
        a = response.a
        a_in_b = response.a_in_b
        response.overlap_n = response.overlap_n.reverse()
        response.overlap_v = response.overlap_v.reverse()
        response.a = response.b
        response.b = a
        response.a_in_b = response.b_in_a
        response.b_in_a = a_in_b
    else:
        response = None

    return result

def test_poly_poly(a, b, response=None):
    a_points = a.points.copy()
    a_len = len(a_points)

    b_points = b.points.copy()
    b_len = len(b_points)

    for i in range(a_len):
        if is_separating_axis(a.pos, b.pos, a_points, b_points, a.normals[i], response):
            return False

    for i in range(b_len):
        if is_separating_axis(a.pos, b.pos, a_points, b_points, b.normals[i], response):
            return False

    if response:
        response.a = a
        response.b = b
        response.overlap_v = response.overlap_n * response.overlap

    return True


def test(a,b, response = None):
    if isinstance(a,Box): a = a.to_poly()
    if isinstance(b,Box): b = b.to_poly()
    if isinstance(a,Poly) and isinstance(b,Poly):
        return test_poly_poly(a, b, response)
    elif isinstance(a,Circle) and isinstance(b,Circle):
        return test_circle_circle(a, b, response)
    elif isinstance(a,Poly) and isinstance(b, Circle):
        return test_poly_circle(a, b, response)
    elif isinstance(a,Circle) and isinstance(b, Poly):
        return test_circle_poly(a, b, response)
    else:
        raise TypeError("Invalid types for test {}() and {}()".format(a.__class__.__name__,b.__class__.__name__))
