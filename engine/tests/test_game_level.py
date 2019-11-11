import sys
import os
import numpy as np
import copy as copy
import random

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform
from camera import Camera
from gameLevel import GameLevel
from force import Gravity
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_size_level():
    v1 = Vector(-1,-1)
    v2 = Vector(1,-1)
    v3 = Vector(1,1)
    v4 = Vector(-1,1)
    p = Polygon([v1,v2,v3,v4])
    plat1 = SolidPlatform(p)
    plat1.translate(Vector(x,y))
    p2 = p.copy()
    p2.translate(Vector(3,2))
    plat2 = SolidPlatform(p2)
    gl = GameLevel([plat1,plat2])
    assert gl.size_level == (0,4,0,3)

def test_physics_step1():
    v1 = Vector(0,0)
    v2 = Vector(1,0)
    v3 = Vector(1,1)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    plat1 = SolidPlatform(p)
    gravity = Gravity(10)
    plat1.add_force(gravity)
    gl = GameLevel([plat1])
    gl.physics_step(1)
    assert plat1.get_position() == Vector(0,-10)
    p2 = p.copy()
    p2.translate(Vector(0,-10))
    assert plat1.get_hit_box() == p2

def test_physics_step2():
    #Check collision with rigid body and gravity
    v1 = Vector(0,0)
    v2 = Vector(1,0)
    v3 = Vector(1,1)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    plat1 = SolidPlatform(p)
    p2 = p.copy()
    p2.translate(Vector(0,-2))
    plat2 = SolidPlatform(p2)
    gravity = Gravity(10)
    plat1.add_force(gravity)
    print(plat1.get_hit_box())
    print(plat2.get_hit_box())
    gl = GameLevel([plat1,plat2])
    for i in range(100):
        gl.physics_step(0.01)
        print(plat1.get_hit_box())
        print(plat2.get_hit_box())
    assert False
