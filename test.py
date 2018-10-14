from collision import Circle, Poly, vec, Response, collide
import collision

import time

a = Poly(vec(0,0), [vec(0,0), vec(0,1), vec(1,2),vec(2,2),vec(2,3), vec(1,3),vec(0,3)])

b = Poly.from_box(vec(0,0), 4,4)

r = Response()
c =  collide(a, b, r)

print("COLLIDED:",c,f"\n{r}")

n = 10000

st = time.time()


for i in range(n):
    #a.angle += 1
    c = collide(a, b, r)


et = time.time()


print('{0:.10f}'.format((et-st)/n))
