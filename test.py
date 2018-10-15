from collision import Circle, Poly, vec, Response, collide, Concave_Poly
import collision

import time

a = Concave_Poly(vec(0,0), [vec(-80,0), vec(-20,20), vec(0,80), vec(20,20), vec(80,0),  vec(20,-20), vec(0,-80), vec(-20,-20)])
b = Concave_Poly(vec(50,50), [vec(-80,0), vec(-20,20), vec(0,80), vec(20,20), vec(80,0),  vec(20,-20), vec(0,-80), vec(-20,-20)])


r = Response()
c =  collide(a, b, r)

print("COLLIDED:",c,f"\n{r}")

n = 1000

st = time.time()


for i in range(n):
    c = collide(a, b)


et = time.time()


print('{0:.10f} PER COLLISION'.format((et-st)/n))
