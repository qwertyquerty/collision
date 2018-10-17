import pygame as pg
import sys
from collision import *

SCREENSIZE = (500,500)

screen = pg.display.set_mode(SCREENSIZE, pg.DOUBLEBUF|pg.HWACCEL)

v = Vector

p0 = Concave_Poly(v(0,0), [v(-80,0), v(-20,20), v(0,80), v(20,20), v(80,0),  v(20,-20), v(0,-80), v(-20,-20)])
p1 = Concave_Poly(v(500,500), [v(-80,0), v(-20,20), v(0,80), v(20,20), v(80,0),  v(20,-20), v(0,-80), v(-20,-20)])

clock = pg.time.Clock()

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    screen.fill((0,0,0))

    p0.pos.x += 1
    p0.pos.y += 0.75
    p0.angle += 0.005
    p1.pos.x -= 0.6
    p1.pos.y -= 0.5

    p0c, p1c, p2c = (0,255,255),(0,255,255),(0,255,255)
    p0bc = (255,255,255)
    p1bc = (255,255,255)

    if collide(p0,p1): p1c = (255,0,0); p0c = (255,0,0);
    if test_aabb(p0.aabb,p1.aabb): p1bc = (255,0,0); p0bc = (255,0,0);

    pg.draw.polygon(screen, p0c, p0.points, 3)
    pg.draw.polygon(screen, p1c, p1.points, 3)

    pg.draw.polygon(screen, p0bc, (p0.aabb[0],p0.aabb[1],p0.aabb[3],p0.aabb[2]), 3)
    pg.draw.polygon(screen, p1bc, (p1.aabb[0],p1.aabb[1],p1.aabb[3],p1.aabb[2]), 3)

    pg.display.flip()


    clock.tick(100)
