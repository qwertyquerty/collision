import math

from .circle import Circle
from .poly import Poly, Concave_Poly
from .response import Response
from .util import Vector, flatten_points_on, voronoi_region, is_separating_axis


LEFT_VORONOI_REGION = -1
MIDDLE_VORONOI_REGION = 0
RIGHT_VORONOI_REGION = 1
RESPONSE = Response()
TEST_POINT = Poly(Vector(0, 0), [Vector(0, 0), Vector(0.0000001, 0.0000001)])


def test_aabb(b1,b2):
    return b1[0][0] <= b2[1][0] and b2[0][0] <= b1[1][0] and b1[0][1] <= b2[2][1] and b2[0][1] <= b1[2][1]

def point_in_circle(p, c):
    difference_v = p - c.pos

    radius_sq = c.radius * c.radius

    distance_sq = difference_v.ln2()

    return distance_sq <= radius_sq


def point_in_poly(p, poly):
    TEST_POINT.pos.set(p)
    RESPONSE.reset()

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
        if difference_v.ln2() != 0:
            response.overlap_n = difference_v.normalize()
            response.overlap_v = response.overlap_n * response.overlap
        else:
            response.overlap_n = Vector(0, 1)
            response.overlap_v = Vector(0, response.overlap)
        response.a_in_b = a.radius <= b.radius and dist <= b.radius - a.radius
        response.b_in_a = b.radius <= a.radius and dist <= a.radius - b.radius

    return True


def test_poly_circle(polygon, circle, response = None):
    circle_pos = circle.pos - polygon.pos
    radius = circle.radius
    radius2 = radius * radius
    points = polygon.rel_points
    ln = len(points)

    for i in range(ln):
        nextn = 0 if i == ln - 1 else i + 1
        prevn = ln - 1 if i == 0 else i - 1

        overlap = 0
        overlap_n = None

        edge = polygon.edges[i].copy()
        point = circle_pos - points[i]

        if response and point.ln2() > radius2:
            response.a_in_b = False

        region = voronoi_region(edge,point)

        if region == LEFT_VORONOI_REGION:
            edge.set(polygon.edges[prevn])

            point2 = circle_pos - points[prevn]

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
            edge.set(polygon.edges[nextn])
            point = circle_pos - points[nextn]
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
            response.overlap_n.set(overlap_n)

    if response:
        response.a = polygon
        response.b = circle
        response.overlap_v = response.overlap_n * response.overlap

    return True


def test_circle_poly(circle,polygon,response=None):
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
    a_points = a.rel_points
    b_points = b.rel_points
    a_pos = a.pos
    b_pos = b.pos

    for n in a.normals:
        if is_separating_axis(a_pos, b_pos, a_points, b_points, n, response):
            return False

    for n in b.normals:
        if is_separating_axis(a_pos, b_pos, a_points, b_points, n, response):
            return False

    if response:
        response.a = a
        response.b = b
        response.overlap_v = response.overlap_n * response.overlap

    return True


def point_in_concave_poly(p, poly):
    TEST_POINT.pos.set(p)

    for tri in poly.tris:
        result = test_poly_poly(TEST_POINT, tri)
        if result:
            return result

    return result


def test_concave_poly_concave_poly(a, b):
    a_pos = a.pos
    b_pos = b.pos

    for a_tri in a.tris:
        for b_tri in b.tris:
            test = True
            for n in a_tri.normals:
                if is_separating_axis(a_pos, b_pos, a_tri.rel_points, b_tri.rel_points, n):
                    test = False

            for n in b_tri.normals:
                if is_separating_axis(a_pos, b_pos, a_tri.rel_points, b_tri.rel_points, n):
                    #print("YIKES 2")
                    test = False

            if test:
                return True

    return False


def test_concave_poly_poly(a, b):
    b_points = b.rel_points
    a_pos = a.pos
    b_pos = b.pos

    for a_tri in a.tris:
        test = True
        for n in a_tri.normals:
            if is_separating_axis(a_pos, b_pos, a_tri.rel_points, b_points, n):
                test = False

        for n in b.normals:
            if is_separating_axis(a_pos, b_pos, a_tri.rel_points, b_points, n):
                test = False

        if test:
            return True

    return False


def test_concave_poly_circle(concave_poly, circle):
    for polygon in concave_poly.tris:
        test = True
        circle_pos = circle.pos - polygon.pos
        radius = circle.radius
        radius2 = radius * radius
        points = polygon.rel_points
        ln = len(points)

        for i in range(ln):
            next = 0 if i == ln - 1 else i + 1
            prev = ln - 1 if i == 0 else i - 1
            overlap = 0
            overlap_n = None
            edge = polygon.edges[i].copy()
            point = circle_pos - points[i]
            region = voronoi_region(edge,point)

            if region == LEFT_VORONOI_REGION:
                edge.set(polygon.edges[prev])
                point2 = circle_pos - points[prev]
                region = voronoi_region(edge, point2)

                if region == RIGHT_VORONOI_REGION:
                    dist = point.ln()

                    if dist > radius:
                        test = False

            elif region == RIGHT_VORONOI_REGION:
                edge.set(polygon.edges[next])
                point = circle_pos - points[next]
                region = voronoi_region(edge,point)

                if region == LEFT_VORONOI_REGION:
                    dist = point.ln()
                    if dist > radius:
                        test = False

            else:
                normal = edge.perp().normalize()
                dist = point.dot(normal)
                dist_abs = abs(dist)

                if dist > 0 and dist_abs > radius:
                    test = False

        if test:
            return True

    return False


def collide(a, b, response=None):
    if isinstance(a, Circle) and isinstance(b, Circle):
        return test_circle_circle(a, b, response)

    if not test_aabb(a.aabb, b.aabb):
        return False


    if isinstance(a, Poly) and isinstance(b, Poly):
        return test_poly_poly(a, b, response)
    elif isinstance(a, Poly) and isinstance(b, Circle):
        return test_poly_circle(a, b, response)
    elif isinstance(a, Circle) and isinstance(b, Poly):
        return test_circle_poly(a, b, response)
    elif isinstance(a, Concave_Poly) and isinstance(b, Concave_Poly):
        return test_concave_poly_concave_poly(a, b)
    elif isinstance(a, Concave_Poly) and isinstance(b, Poly):
        return test_concave_poly_poly(a, b)
    elif isinstance(a, Poly) and isinstance(b, Concave_Poly):
        return test_concave_poly_poly(b, a)
    elif isinstance(a, Concave_Poly) and isinstance(b, Circle):
        return test_concave_poly_circle(a, b)
    elif isinstance(a, Circle) and isinstance(b, Concave_Poly):
        return test_concave_poly_circle(b, a)
    else:
        raise TypeError("Invalid types for collide {}() and {}()".format(a.__class__.__name__,b.__class__.__name__))
