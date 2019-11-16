import sys
import os
import numpy as np
import pygame

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform
from gameLevel import GameLevel
from hypothesis import given
from hypothesis.strategies import integers, lists

pygame.init()
fen = pygame.display.set_mode((600, 600),0)

#Coordinates for the Rhombus

rhx = 1200
rhy = 200
rhs = 40#size
#Let's start by creating the polygon for hit_boxes
v1 = Vector(-rhs,0) #Creates a point -> NEVER MAKE A POINT IN 0,0 !!!
v2 = Vector(0,-rhs)
v3 = Vector(0,rhs)
v4 = Vector(rhs,0)
rh = Polygon([v1,v3,v4,v2]) #Creates the polygon corresponding to the given sequence
#It's a rhombus
prh = SolidPlatform(rh)
prh.translate(Vector(rhx,rhy))


largeur = 600
epf = 150 + largeur#ecart inter plateforme

rec = Rectangle(-300,-400,largeur,800)
pr = SolidPlatform(rec)
pr.translate(Vector(-200,800))

L = []

for i in range(10):
    L.append(SolidPlatform(rec.copy()))

    if i == 0:
        L[i].translate(Vector(600,800))
    else:
        L[i].translate(Vector(epf+L[-2].get_position().x,800))
gl = GameLevel(L+[pr,prh],[])
gl.load_camera(fen) #Load the camera in the window fen
gl.get_camera().set_dimension(Vector(2000,2000)) #Resize the camera
gl.get_camera().set_position(Vector(0,-1000)) #Resize the camera
gl.aff()
pygame.time.wait(2000)
pygame.display.quit()


