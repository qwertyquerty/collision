import math

from . import poly
from .util import vec


POLY_RECALC_ATTRS = ["r"]

class Circle():
    def __init__(self,pos,r):
        self.pos = pos
        self.radius = r

    def get_aabb(self):
        r = self.radius
        return poly.Poly.from_box(this.pos, r*2, r*2)

    def __str__(self):
        r = "Circle [\n\tradius = {}\n\tpos = {}\n]".format(self.radius, self.pos)
        return r


    def __repr__(self):
        return self.__str__()
