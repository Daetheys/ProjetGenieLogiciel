import sys
import os
import numpy as np
import copy as copy
import random
import pygame

path = os.getcwd()
sys.path.append(path + "/engine")
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform
from camera import Camera
from gameLevel import GameLevel
from force import Gravity
from hitbox import Hitbox
from rect import Rect
from hypothesis import given
from hypothesis.strategies import integers, lists

pygame.init()
fen = pygame.display.set_mode((500, 500),0)

def test_size_level():
    v1 = Vector(-1,-1)
    v2 = Vector(1,-1)
    v3 = Vector(1,1)
    v4 = Vector(-1,1)
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    Hb2 = Hb.copy()
    plat2 = SolidPlatform(Hb2)
    plat2.translate(Vector(3,2))
    gl = GameLevel([plat1,plat2],[])
    pass

def test_physics_step1():
    R = Rect(-1,-1,2,2)
    plat1 = SolidPlatform(R)
    gravity = Gravity(10)
    plat1.add_force(gravity)
    gl = GameLevel([plat1],[])
    gl.physics_step(1)
    assert plat1.get_position() == Vector(0,10)
    p2 = p.copy()
    p2.translate(Vector(0,10))
    print(plat1.get_hit_box(),p2)
    assert plat1.get_hit_box() == p2


def test_physics_step2():
    #Check collision with rigid body and gravity
    v1 = Vector(-1,-1)
    v2 = Vector(1,-1)
    v3 = Vector(1,1)
    v4 = Vector(-1,1)
    p = Polygon([v1,v2,v3,v4])
    p.rotate(np.pi/3)
    plat1 = SolidPlatform(p)
    p2 = p.copy()
    p2.translate(Vector(0.1,10))
    plat2 = SolidPlatform(p2)
    gravity = Gravity(10)
    plat1.add_force(gravity)
    gl = GameLevel([plat1,plat2],[])
    for i in range(7):
        gl.physics_step(0.01)
    v = plat2.get_position()
    print(v)
    assert v.y < 12

