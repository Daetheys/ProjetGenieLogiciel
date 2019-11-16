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
fen = pygame.display.set_mode((500, 500),0)

#Coordinates for the platform
x = 1
y = 1

#Let's start by creating the polygon for hit_boxes
v1 = Vector(-1,-1) #Creates a point
v2 = Vector(1,-1)
v3 = Vector(1,1)
v4 = Vector(-1,1)
p = Polygon([v1,v2,v3,v4])*2 #Creates the polygon corresponding to the given sequence -> it's a rectangle

#Now let's build the platform associated to this polygon and move it to our coordinates
plat = SolidPlatform(p)
plat.translate(Vector(x,y))

x2 = 0
y2 = 8

#To create an other platform with the same hit box it easy:
p2 = p.copy() #It's very important to copy it and not using p or both platform would be linked (if one of them is moving to other will too)
plat.rotate(np.pi/5)

plat2 = SolidPlatform(p2)
plat2.translate(Vector(x2,y2))

plat2.rotate(np.pi/5)
plat2.set_speed(Vector(0,-0.5))

gl = GameLevel([plat,plat2],[])
gl.load_camera(fen) #Load the camera in the window fen
gl.get_camera().set_dimension(Vector(25,25)) #Resize the camera
gl.get_camera().set_position(Vector(-12,-5))
gl.aff()
for i in range(10):
    gl.refresh(0.001)
    pygame.time.wait(50)

pygame.time.wait(500)
