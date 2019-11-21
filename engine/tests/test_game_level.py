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
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    gravity = Gravity(10)
    plat1.add_force(gravity)
    gl = GameLevel([plat1],[])
    gl.physics_step(1)
    assert plat1.get_position() == Vector(0,10)
    assert plat1.get_hit_box().get_world_poly() == Polygon([Vector(-1,9),Vector(1,9),Vector(1,11),Vector(-1,11)])


def test_physics_step2():
    #Check collision with rigid body and gravity
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    
    plat2 = plat1.copy()
    plat2.translate(Vector(0.1,10))
    plat1.rotate(np.pi/4)
    
    gravity = Gravity(10)
    plat1.add_force(gravity)
    
    gl = GameLevel([plat1,plat2],[])
    
    for i in range(7):
        gl.physics_step(0.01)
        
    v = plat2.get_position()
    
    print(v)
    assert v.y < 12


def test_opti():
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    plat = [plat1]
    for i in range(100):
        plat.append(plat[-1].copy())
        plat[-1].translate(Vector(10,0))
    gl = GameLevel(plat,[])
