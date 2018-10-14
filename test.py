from collision import Circle, Poly, vec, Response, collide
import collision

import time

a = Poly(vec(0,0), [vec(0,0), vec(0,5),vec(5,5)])
print(a.normals)
b = Circle(vec(0,11), 5)

r = Response()
c =  collide(a, b, r)

print("COLLIDED:",c,f"\n{r}")

n = 10000

st = time.time()


for i in range(n):
    a.angle += 1
    c = collide(a, b, r)


et = time.time()


print('{0:.10f}'.format((et-st)/n))
