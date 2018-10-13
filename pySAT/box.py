import math

from . import poly

from .util import vec

class Box():
    def __init__(self, pos, w, h):
        self.pos = pos
        self.w = w
        self.h = h

    def to_poly(self):
        return poly.Poly(vec(self.pos.x,self.pos.y), [vec(0,0),vec(self.w,0), vec(self.w,self.h), vec(0,self.h)])

    def __str__(self):
        r = "Box [\n\tpos = {}\n\tw = {}\n\th = {}\n]".format(self.pos,self.w,self.h)
        return r


    def __repr__(self):
        return self.__str__()
