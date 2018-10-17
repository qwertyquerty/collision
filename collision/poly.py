import math

from .util import Vector
from . import tripy

POLY_RECALC_ATTRS = ["angle"]


class Poly:
    def __init__(self, pos, points, angle=0):
        self.pos = pos
        self.__dict__["angle"] = angle
        self.set_points(points)

    @classmethod
    def from_box(cls, center, width, height):
        hw = width / 2
        hh = height / 2
        c = cls(center, [Vector(-hw, -hh), Vector(hw, -hh), Vector(hw, hh), Vector(-hw, hh)])
        return c

    def __setattr__(self, key, val):
        self.__dict__[key] = val
        if key in POLY_RECALC_ATTRS:
            self._recalc()

    def set_points(self, points):
        if tripy.is_clockwise(points):
            points = points[::-1]

        length_changed = len(self.base_points) != len(points) if hasattr(self, "base_points") else True
        if length_changed:
            self.rel_points = []
            self.edges = []
            self.normals = []

            for i in range(len(points)):
                self.rel_points.append(Vector(0, 0))
                self.edges.append(Vector(0, 0))
                self.normals.append(Vector(0, 0))

        self.base_points = points
        self._recalc()

    def _recalc(self):
        l = range(len(self.base_points))

        for i in l:
            self.rel_points[i].set(self.base_points[i])
            if self.angle != 0:
                self.rel_points[i] = self.rel_points[i].rotate(self.angle)

        for i in l:
            p1 = self.rel_points[i]
            p2 = self.rel_points[i+1] if i < len(self.rel_points) - 1 else self.rel_points[0]

            e = self.edges[i] = p2-p1

            self.normals[i] = e.perp().normalize()


    @property
    def points(self):
        pos = self.pos
        return [pos+point for point in self.rel_points]

    @property
    def aabb(self):
        points = self.points
        x_min = points[0].x
        y_min = points[0].y
        x_max = points[0].x
        y_max = points[0].y

        for point in points:
            if point.x < x_min: x_min = point.x
            elif point.x > x_max: x_max = point.x
            if point.y < y_min: y_min = point.y
            elif point.y > y_max: y_max = point.y

        return ((x_min,y_min), (x_max,y_min), (x_min,y_max), (x_max,y_max))


    def get_centroid(self):
        cx = 0
        cy = 0
        ar = 0
        for i in range(len(self.rel_points)):
            p1 = self.rel_points[i]
            p2 = self.rel_points[0] if i == len(self.rel_points) - 1 else self.rel_points[i+1]
            a = p1.x * p2.y - p2.x * p1.y
            cx += (p1.x + p2.x) * a
            cy += (p1.x + p2.y) * a
            ar += a

        ar = ar * 3
        cx = cx / ar
        cy = cy / ar

        return Vector(cx, cy)

    def __str__(self):
        r = "Poly [\n\tpoints = [\n"
        for p in self.points:
            r += "\t\t{}\n".format(str(p))
        r += "\t]\n"
        r += "\tpos = {}\n\tangle = {}\n".format(self.pos, self.angle)
        r += "]"
        return r

    def __repr__(self):
        return self.__str__()


class Concave_Poly():
    def __init__(self, pos, points, angle=0):
        self.pos = pos
        self.__dict__["angle"] = angle
        self.set_points(points)

    def __setattr__(self, key, val):
        self.__dict__[key] = val
        if key in POLY_RECALC_ATTRS:
            self._recalc()

    def set_points(self, points):
        if tripy.is_clockwise(points):
            points = points[::-1]

        length_changed = len(self.base_points) != len(points) if hasattr(self,"base_points") else True
        if length_changed:
            self.rel_points = []
            self.tris = []
            self.edges = []
            self.normals = []

            for i in range(len(points)):
                self.rel_points.append(Vector(0,0))
                self.edges.append(Vector(0,0))
                self.normals.append(Vector(0,0))

        self.base_points = points
        self._calculate_tris()
        self._recalc()

    def _recalc(self):
        l = range(len(self.base_points))

        for i in l:
            self.rel_points[i].set(self.base_points[i])
            if self.angle != 0:
                self.rel_points[i] = self.rel_points[i].rotate(self.angle)

        for i in l:
            p1 = self.rel_points[i]
            p2 = self.rel_points[i+1] if i < len(self.rel_points) - 1 else self.rel_points[0]

            e = self.edges[i] = p2-p1

            self.normals[i] = e.perp().normalize()

        self._update_tris()

    def _calculate_tris(self):
        self.tris = [Poly(self.pos, points, self.angle) for points in tripy.earclip(self.base_points)]

    def _update_tris(self):
        for tri in self.tris:
            tri.angle = self.angle
            tri.pos = self.pos

    @property
    def points(self):
        templist = []
        for p in self.rel_points:
            templist.append(p+self.pos)
        return templist

    @property
    def aabb(self):
        points = self.points
        x_min = points[0].x
        y_min = points[0].y
        x_max = points[0].x
        y_max = points[0].y

        for point in points:
            if point.x < x_min: x_min = point.x
            elif point.x > x_max: x_max = point.x
            if point.y < y_min: y_min = point.y
            elif point.y > y_max: y_max = point.y

        return ((x_min,y_min), (x_max,y_min), (x_min,y_max), (x_max,y_max))



    def get_centroid(self):
        cx = 0
        cy = 0
        ar = 0
        for i in range(len(self.rel_points)):
            p1 = self.rel_points[i]
            p2 = self.rel_points[0] if i == len(self.rel_points) - 1 else self.rel_points[i+1]
            a = p1.x * p2.y - p2.x * p1.y
            cx += (p1.x + p2.x) * a
            cy += (p1.x + p2.y) * a
            ar += a

        ar = ar * 3
        cx = cx / ar
        cy = cy / ar

        return Vector(cx, cy)

    def __str__(self):
        r = "Concave_Poly [\n\tpoints = [\n"
        for p in self.points:
            r+= "\t\t{}\n".format(str(p))
        r += "\t]\n"
        r += "\tpos = {}\n\tangle = {}\n".format(self.pos, self.angle)
        r += "]"
        return r

    def __repr__(self):
        return self.__str__()
