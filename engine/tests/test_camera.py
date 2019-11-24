import sys
import os
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from camera import Camera
from spriteNode import SpriteNode
from collideTransformable import CollideTransformable
from rect import Rect
from hitbox import Hitbox
from hypothesis import given
from hypothesis.strategies import integers, lists

import pygame

def cut(v):
    if abs(v)>10**5:
        if v > 0:
            return 10**5
        else:
            return -10**5
    return v

@given(integers(),integers(),integers(),integers())
def test_set_get(x,y,w,h):
    x = cut(x) #Cut too high values or numpy doesn't work
    y = cut(y)
    w = cut(w)
    h = cut(h)
    c = Camera()
    c.set_position(Vector(x,y))
    c.set_dimension(Vector(w,h))
    assert c.get_position() == Vector(x,y)
    assert c.get_dimension() == Vector(w,h)

def test_is_in_camera():
    c = Camera()
    c.set_position(Vector(0,0))
    c.set_dimension(Vector(10,5))
    v1 = Vector(0,0)
    v2 = Vector(1,0)
    v3 = Vector(1,1)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    assert c.is_in_camera(p)
    v1 = Vector(-2,-1)
    v2 = Vector(-3,-5)
    v3 = Vector(-4,-1)
    p = Polygon([v1,v2,v3])
    assert not(c.is_in_camera(p))
    v1 = Vector(10,5)
    v2 = Vector(10,0)
    v3 = Vector(15,2)
    p = Polygon([v1,v2,v3])
    assert c.is_in_camera(p)
    v1 = Vector(0,5.1)
    v2 = Vector(9,5.001)
    v3 = Vector(5,15)
    p = Polygon([v1,v2,v3])
    assert not(c.is_in_camera(p))
    c.set_dimension(Vector(2,15))
    assert c.is_in_camera(p)

def test_pos_in_camera():
    pygame.init()
    fen = pygame.display.set_mode((500, 500),0)
    
    S = CollideTransformable()
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    S.set_hit_box(Hb)
    C = Camera()
    C.set_position(Vector(-1,-1))
    C.set_dimension(Vector(4,4))
    C.set_fen(fen)
    pos_vect = S.get_pos_camera(C.get_distorsion(),S.get_hit_box())
    assert pos_vect == Polygon([Vector(0,0),Vector(250,0),Vector(250,250),Vector(0,250)])
