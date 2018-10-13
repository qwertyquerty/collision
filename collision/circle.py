import math

from . import box
from .util import vec


POLY_RECALC_ATTRS = ["r"]

class Circle():
    def __init__(self,pos,r):
        self.pos = pos
        self.radius = r

    def get_aabb(self):
        r = self.radius
        corner = this.pos - vec(r,r)
        return box.Box(corner, r*2, r*2).to_poly()

    def __str__(self):
        r = "Circle [\n\tradius = {}\n\tpos = {}\n]".format(self.radius, self.pos)
        return r


    def __repr__(self):
        return self.__str__()
