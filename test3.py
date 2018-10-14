from collision import *
import time
p0 = Concave_Poly(vec(0,0), [vec(0,0), vec(100,0), vec(100,100), vec(50,50), vec(0,100)])
p1 = vec(50,70)


print(point_in_poly(p1,p0))
