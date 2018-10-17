import math

from . import poly
from .util import Vector

CIRCLE_RECALC_ATTRS = ["r"]


class Circle:
    def __init__(self,pos,r):
        self.pos = pos
        self.radius = r
        self._recalc()

    def __setattr__(self,key,val):
        self.__dict__[key] = val
        if key in CIRCLE_RECALC_ATTRS:
            self._recalc()

    def _recalc(self):
        self.aabb = self.get_aabb()

    def get_aabb(self):
        r = self.radius
        pos = self.pos
        return ((pos.x-r, self.pos.y-r), (pos.x+r,self.pos.y-r), (pos.x+r, self.pos.y+r), (pos.x-r, pos.y+r))

    def __str__(self):
        r = "Circle [\n\tradius = {}\n\tpos = {}\n]".format(self.radius, self.pos)
        return r

    def __repr__(self):
        return self.__str__()
