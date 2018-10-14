import pygame as pg
import sys
from collision import *



SCREENSIZE = (500,500)

screen = pg.display.set_mode(SCREENSIZE, pg.DOUBLEBUF|pg.HWACCEL)

p0 = Concave_Poly(vec(0,0), [vec(0,0), vec(100,0), vec(100,100), vec(50,20),  vec(0,100)])
p1 = Circle(vec(500,500), 20)
p2 = Poly(vec(0,0), [vec(-20,-20), vec(20,-20), vec(20,20), vec(-20,20)])

clock = pg.time.Clock()


while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()



    screen.fill((0,0,0))

    p0c, p1c, p2c = (255,255,255),(255,255,255),(255,255,255)
    if collide(p0,p1):
        p1c = (255,0,0)
        p0c = (255,0,0)
    if collide(p1,p2):
        p1c = (255,0,0)
        p2c = (255,0,0)
    if collide(p2,p0):
        p2c = (255,0,0)
        p0c = (255,0,0)


    pg.draw.polygon(screen, p0c, p0.abs_points, 3)
    pg.draw.polygon(screen, p2c, p2.abs_points, 3)
    pg.draw.circle(screen, p1c, vec(int(p1.pos.x),int(p1.pos.y)), int(p1.radius), 3)

    #for t in p0.tris:
    #    pg.draw.polygon(screen, p0c, t.abs_points, 3)
    #for t in p1.tris:
    #    pg.draw.polygon(screen, p1c, t.abs_points, 3)


    pg.display.flip()


    p0.pos.x += 1
    p0.pos.y += 0.75
    p0.angle += 0.005

    p1.pos.x -= 0.6
    p1.pos.y -= 0.5

    p2.pos = vec(*pg.mouse.get_pos())
    p2.angle += 0.05

    clock.tick(60)
