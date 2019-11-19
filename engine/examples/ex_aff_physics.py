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
from rect import Rect
from force import Gravity
from hypothesis import given
from hypothesis.strategies import integers, lists

from hit_box import HitBox

pygame.init()
fen = pygame.display.set_mode((500, 500),0)

#Coordinates for the platform
x = -5
y = 1

#Let's start by creating the polygon for hit_boxes

p = Rect(-1,-1,2,2) #Creates the polygon corresponding to the given sequence -> it's a rectangle
hb = HitBox(p)
#Now let's build the platform associated to this polygon and move it to our coordinates
plat = SolidPlatform(hb)
plat.set_sps(None)
plat.translate(Vector(x,y))
plat.rotate(np.pi/4)

x2 = -6
y2 = 5

#To create an other platform with the same hit box it easy:
hb2 = hb.copy()
plat2 = SolidPlatform(hb2)
plat2.set_sps(None)
plat2.translate(Vector(10,5))

hb3 = hb2.copy()
plat3 = SolidPlatform(hb3)
plat3.set_sps(None)
plat3.translate(Vector(10.5,1))

hb4 = hb2.copy()
plat4 = SolidPlatform(hb4)
plat4.set_sps(None)
plat4.translate(Vector(9,10))

gravity = Gravity(10)

#plat2.rotate(np.pi/5)
#plat2.add_force(gravity)
plat.add_force(gravity)
plat2.add_force(gravity)
plat3.add_force(gravity)

gl = GameLevel([plat,plat2,plat3,plat4],[])
gl.load_camera(fen) #Load the camera in the window fen
gl.get_camera().set_dimension(Vector(50,50)) #Resize the camera
gl.get_camera().set_position(Vector(-12,-12))
gl.aff()
for i in range(100):
    print(i)
    gl.refresh(0.001)
    #pygame.time.wait(500)

pygame.time.wait(500)
