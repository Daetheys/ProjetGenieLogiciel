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
y = 6

#Let's start by creating the polygon for hit_boxes
v1 = Vector(0,0) #Creates a point -> NEVER CREATE A POINT IN (0,0) !
v2 = Vector(0,-1)
v3 = Vector(2,-1)
v4 = Vector(2,0)
p = Polygon([v1,v2,v3,v4]) #Creates the polygon corresponding to the given sequence -> it's a rectangle

#Now let's build the platform associated to this polygon and move it to our coordinates
plat = SolidPlatform(p)
plat.translate(Vector(x,y))

x2 = 7
y2 = 5

#To create an other platform with the same hit box it easy:
p2 = p.copy() #It's very important to copy it and not using p or both platform would be linked (if one of them is moving to other will too)
plat2 = SolidPlatform(p2)
plat2.translate(Vector(x2,y2))

gl = GameLevel([plat,plat2],[])
gl.load_camera(fen) #Load the camera in the window fen
gl.get_camera().set_dimension(Vector(10,10)) #Resize the camera
gl.aff()
pygame.time.wait(5000)
pygame.display.quit()
