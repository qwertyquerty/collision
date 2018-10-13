from collision import Circle, Box, Poly, vec, Response, collide
import collision

import time

a = Box(vec(-2,-2), 4,4).to_poly()

b = Box(vec(-2,-1), 4, 4).to_poly()

r = Response()




c =  collide(a, b, r)

print("COLLIDED:",c,f"\n{r}")

n = 10000

st = time.time()


for i in range(n):
    c = collide(a, b, r)


et = time.time()


print('{0:.10f}'.format((et-st)/n))
