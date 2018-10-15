from collision import *
import time
p0 = Concave_Poly(vec(0,0), [vec(0,0), vec(100,0), vec(100,100), vec(50,50), vec(0,100)])


p1 = vec(50,70)
print(point_in_concave_poly(p1,p0))

p1 = vec(50,40)
print(point_in_concave_poly(p1,p0))
