import math

from .util import vec

class Response():
    def __init__(self):
        self.reset()

    def reset(self):
        self.a = None
        self.b = None
        self.overlap_n = vec(0,0)
        self.overlap_v = vec(0,0)
        self.a_in_b = True
        self.b_in_a = True
        self.overlap = math.inf
        return self

    def __str__(self):
        r = "Response [\n\ta = {}\n\tb = {}\n\toverlap = {}\n\toverlap_n = {}\n\toverlap_v = {}\n\ta_in_b = {}\n\tb_in_a = {}\n]".format("\n\t".join(str(self.a).split("\n"))+"\n", "\n\t".join(str(self.b).split("\n"))+"\n", self.overlap, self.overlap_n, self.overlap_v, self.a_in_b, self.b_in_a)
        return r

    def __repr__(self):
        return self.__str__()
