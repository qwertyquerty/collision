import pygame as pg
import sys
from collision import *

SCREENSIZE = (500,500)

screen = pg.display.set_mode(SCREENSIZE, pg.DOUBLEBUF|pg.HWACCEL)

p0 = Concave_Poly(vec(0,0), [vec(-80,0), vec(-20,20), vec(0,80), vec(20,20), vec(80,0),  vec(20,-20), vec(0,-80), vec(-20,-20)])
p1 = Concave_Poly(vec(500,500), [vec(-80,0), vec(-20,20), vec(0,80), vec(20,20), vec(80,0),  vec(20,-20), vec(0,-80), vec(-20,-20)])

print(p1)

clock = pg.time.Clock()

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    screen.fill((0,0,0))

    p0c, p1c, p2c = (0,255,255),(0,255,255),(0,255,255)
    if collide(p0,p1):
        p1c = (255,0,0)
        p0c = (255,0,0)

    #pg.draw.polygon(screen, p0c, p0.abs_points, 6)
    #pg.draw.polygon(screen, p1c, p1.abs_points, 6)


    for t in p0.tris:
        pg.draw.polygon(screen, p0c, t.points, 3)
    for t in p1.tris:
       pg.draw.polygon(screen, p1c, t.points, 3)


    pg.display.flip()

    p0.pos.x += 1
    p0.pos.y += 0.75
    p0.angle += 0.005

    p1.pos.x -= 0.6
    p1.pos.y -= 0.5

    clock.tick(100)
