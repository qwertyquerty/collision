import math


from .util import vec
from . import tripy

POLY_RECALC_ATTRS = ["angle"]

class Poly():
    def __init__(self,pos,points,angle=0):
        self.__dict__["pos"] = pos
        self.__dict__["angle"] = angle
        self.set_points(points)

    @classmethod
    def from_box(cls, center, width, height):
        hw = width / 2
        hh = height / 2
        c = cls(center, [vec(-hw, -hh), vec(hw, -hh), vec(hw, hh), vec(-hw, hh)])
        return c

    def __setattr__(self,key,val):
        self.__dict__[key] = val
        if key in POLY_RECALC_ATTRS:
            self._recalc()


    def set_points(self,points):
        if tripy.is_clockwise(points):
            points = points[::-1]

        length_changed = len(self.base_points) != len(points) if hasattr(self,"base_points") else True
        if length_changed:
            self.points = []
            self.edges = []
            self.normals = []

            for i in range(len(points)):
                self.points.append(vec(0,0))
                self.edges.append(vec(0,0))
                self.normals.append(vec(0,0))

        self.base_points = points
        self._recalc()


    def rotate(self,angle):
        for i in range(len(self.base_points)):
            self.base_points[i] = self.base_points[i].rotate(angle)

        self._recalc()



    def translate(self,v):
        for i in range(len(self.base_points)):
            self.base_points[i] += v

        self._recalc()


    def _recalc(self):
        l = range(len(self.base_points))

        for i in l:
            self.points[i].set(self.base_points[i])
            if self.angle != 0:
                self.points[i] = self.points[i].rotate(self.angle)

        for i in l:
            p1 = self.points[i]
            p2 = self.points[i+1] if i < len(self.points) - 1 else self.points[0]

            e = self.edges[i] = p2-p1

            self.normals[i] = e.perp().normalize()

    @property
    def abs_points(self):
        l = []
        for p in self.points:
            l.append(p+self.pos)
        return l


    def get_aabb(self):
        x_min = self.points[0].x
        y_min = self.points[0].y
        x_max = self.points[0].x
        y_max = self.points[0].y

        for point in self.points:
            if point.x < x_min: x_min = point.x
            elif point.x > x_max: x_max = point.x
            if point.y < y_min: y_min = point.y
            elif point.y > y_max: y_max = point.y

        return Poly.from_box(vec((x_min+x_max)/2, (y_min+y_max)/2), x_max- x_min, y_max - y_min)

    def get_centroid(self):
        cx = 0
        cy = 0
        ar = 0
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[0] if i == len(self.points) -1 else self.points[i+1]
            a = p1.x * p2.y - p2.x * p1.y
            cx += (p1.x + p2.x) * a
            cy += (p1.x + p2.y) * a
            ar += a

        ar = ar * 3
        cx = cx / ar
        cy = cy / ar

        return vec(cx,cy)

    def __str__(self):
        r = "Poly [\n\tabs_points = [\n"
        for p in self.abs_points:
            r+= "\t\t{}\n".format(str(p))
        r += "\t]\n"
        r += "\tpos = {}\n\tangle = {}\n".format(self.pos, self.angle)
        r += "]"
        return r

    def __repr__(self):
        return self.__str__()


class Concave_Poly():
    def __init__(self,pos,points,angle=0):
        self.__dict__["pos"] = pos
        self.__dict__["angle"] = angle
        self.set_points(points)


    def __setattr__(self,key,val):
        self.__dict__[key] = val
        if key in POLY_RECALC_ATTRS:
            self._recalc()
        elif key == "pos":
            self._update_tris()


    def set_points(self,points):
        if tripy.is_clockwise(points):
            points = points[::-1]

        length_changed = len(self.base_points) != len(points) if hasattr(self,"base_points") else True
        if length_changed:
            self.points = []
            self.tris = []
            self.edges = []
            self.normals = []

            for i in range(len(points)):
                self.points.append(vec(0,0))
                self.edges.append(vec(0,0))
                self.normals.append(vec(0,0))

        self.base_points = points
        self._calculate_tris()
        self._recalc()



    def _recalc(self):
        l = range(len(self.base_points))

        for i in l:
            self.points[i].set(self.base_points[i])
            if self.angle != 0:
                self.points[i] = self.points[i].rotate(self.angle)

        for i in l:
            p1 = self.points[i]
            p2 = self.points[i+1] if i < len(self.points) - 1 else self.points[0]

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
    def abs_points(self):
        l = []
        for p in self.points:
            l.append(p+self.pos)
        return l


    def __str__(self):
        r = "Concave_Poly [\n\tabs_points = [\n"
        for p in self.abs_points:
            r+= "\t\t{}\n".format(str(p))
        r += "\t]\n"
        r += "\tpos = {}\n\tangle = {}\n".format(self.pos, self.angle)
        r += "]"
        return r

    def __repr__(self):
        return self.__str__()
