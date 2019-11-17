
import sys
import os
#import numpy as np
import pygame
from pygame.locals import *
path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform,Pattern
from gameLevel import GameLevel
from hypothesis import given
from hypothesis.strategies import integers, lists

def level_1_kshan(g):



    largeur = 600
    epf = 150 + largeur#ecart inter plateforme

    #Coordinates for the Rhombus

    rhx = 2000
    rhy = 0
    rhs = 40#size
    #Let's start by creating the polygon for hit_boxes
    v1 = Vector(-rhs,0) #Creates a point -> NEVER MAKE A POINT IN 0,0 !!!
    v2 = Vector(0,-rhs)
    v3 = Vector(0,rhs)
    v4 = Vector(rhs,0)
    rh = Polygon([v1,v3,v4,v2]) #Creates the polygon corresponding to the given sequence
    #It's a rhombus
    prh = Pattern(rh,"name")
    prh.pt = "UpDown"
    prh.translate(Vector(rhx,rhy))
    prh.speed = 30
    prh.period = 700//prh.speed
    prh2 = prh.copy()
    prh2.translate(Vector(80,0))
    print(str("!!!!")+prh2.pt+str("\n\n !!!\n\n"))

    RH = [prh]
    for _ in range(1,10):
        RH.append(RH[-1].copy())
        RH[-1].translate(Vector(80,0))
        RH[-1].init_delay += 2

    tau = prh.copy()
    tau.pt = "Square"
    RH.append(tau)
    tau.translate(Vector(-1000,200))

    tau.create_sps("spike")
    rec = Rectangle(-300,-400,largeur,800)
    pr = SolidPlatform(rec)
    pr.translate(Vector(-200,800))

    L = [pr]

    for i in range(1,10):
        L.append(SolidPlatform(rec.copy()))

        if i == 1:
            L[i].translate(Vector(600,800))
        else:
            L[i].translate(Vector(epf+L[-2].get_position().x,800))

    gl = GameLevel(L+RH,[])
    gl.load_camera(g.win())#Load the camera in the window fen
    gl.get_camera().set_dimension(Vector(1280,720)) #Resize the camera
    #Usually 2000,2000 (moins de distortion ?) or 2560,1440 (plus grosse résolution)
    gl.get_camera().set_position(Vector(0,0)) #change pos of  the camera
    gl.aff()

    #execution of the level
    t = 0#time
    fps = g.options["FPS"]# FPS is usually 30
    sec_wait = 3
    while t < g.options["FPS"] * sec_wait:#sec_wait seconds to wait
        pygame.time.Clock().tick(g.options["FPS"])
        print(t)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False#You failed.
                if event.key == K_RIGHT:
                    print("amaRIGHT")
                if event.key == K_LEFT:
                    print("amaLEFT")
                    x,y = gl.get_camera().get_position().to_tuple()
                    print((x,y))
                    gl.get_camera().set_position(Vector(x-200,y))

        for pat in RH:
            pat.pattern(t)

        #Updating the camera
        x,y = gl.get_camera().get_position().to_tuple()
        print((x,y))
        gl.get_camera().set_position(Vector(x+40,y))
        gl.aff()
        g.flip()
        t += 1
    #pygame.display.quit()

    return True#You always succeed. perhaps return a score (integer) ?

