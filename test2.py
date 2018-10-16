import pygame as pg
import sys
from collision import Poly, Circle, Response, collide, vec



SCREENSIZE = (500,500)

screen = pg.display.set_mode(SCREENSIZE, pg.DOUBLEBUF|pg.HWACCEL)

p0 = Poly(vec(10,10), [vec(0,0), vec(100,0), vec(50,100)])
p1 = Poly(vec(500,0), [vec(0,500), vec(0,0)])
c = Circle(vec(250,450), 20)

clock = pg.time.Clock()


while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()



    screen.fill((0,0,0))

    p0c, p1c, cc = (255,255,255),(255,255,255),(255,255,255)

    if collide(p0,c):
        p0c = (255,0,0)
        cc = (255,0,0)
    if collide(p1,c):
        p1c = (255,0,0)
        cc = (255,0,0)
    if collide(p1,p0):
        p1c = (255,0,0)
        p0c = (255,0,0)

    pg.draw.polygon(screen, p0c, p0.points, 3)
    pg.draw.polygon(screen, p1c, p1.points, 3)
    pg.draw.circle(screen, cc, c.pos, int(c.radius), 3)
    pg.display.flip()

    p0.angle += 0.01
    p0.pos.x += 1
    p0.pos.y += 0.6

    c.pos.y -= 1
    c.radius += 0.1

    p1.angle += 0.005

    clock.tick(120)
