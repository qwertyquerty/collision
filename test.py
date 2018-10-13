from pySAT import Circle, Box, Poly, vec, Response
import pySAT

import time

a = Poly(vec(0,0), [vec(-10,0),vec(10,0),vec(5,15)])

b = Poly(vec(0,0), [vec(-8,0),vec(8,0),vec(5,5)])

r = Response()




c =  pySAT.test(a, b, r)

print("COLLIDED:",c,f"\n{r}")

n = 10000

st = time.time()


for i in range(n):
    c =  pySAT.test(a, b, r)
    a.angle += 1

et = time.time()


print('{0:.10f}'.format((et-st)/n))
