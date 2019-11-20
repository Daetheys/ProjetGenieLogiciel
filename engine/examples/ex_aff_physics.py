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

from hitbox import Hitbox

pygame.init()
fen = pygame.display.set_mode((500, 500),0)

#Coordinates for the platform
x = 0
y = 10

#Let's start by creating the polygon for hit_boxes

p = Rect(-1,-1,2,2) #Creates the polygon corresponding to the given sequence -> it's a rectangle
hb = Hitbox(p)
#Now let's build the platform associated to this polygon and move it to our coordinates
plat = SolidPlatform(hb)
plat.set_sps(None)
plat.translate(Vector(x,y))


#To create an other platform with the same hit box it easy:
plat2 = plat.copy()
plat3 = plat.copy()
plat4 = plat.copy()
plat2.rot(45)
plat.rotate(np.pi/4)
plat2.translate(Vector(0.5,-10))
plat3.translate(Vector(0.1,-5))
plat4.translate(Vector(0.3,-15))



"""
hb3 = hb.copy()
plat3 = SolidPlatform(hb3)
plat3.set_sps(None)
plat3.translate(Vector(10.5,1))

hb4 = hb.copy()
plat4 = SolidPlatform(hb4)
plat4.set_sps(None)
plat4.translate(Vector(9,10))
"""
gravity = Gravity(1)

#plat2.rotate(np.pi/5)
#plat2.add_force(gravity)
#plat.add_force(gravity)
plat2.add_force(gravity)
plat3.add_force(gravity)
plat4.add_force(gravity)

gl = GameLevel([plat,plat2,plat3,plat4],[])
gl.load_camera(fen) #Load the camera in the window fen
gl.get_camera().set_dimension(Vector(20,20)) #Resize the camera
gl.get_camera().set_position(Vector(-5,-5))
gl.aff()
for i in range(10000):
    gl.refresh(0.01)
    #pygame.time.wait(50)

pygame.time.wait(500)
