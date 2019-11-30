import sys
import os
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
path = os.getcwd()
path += "/error"
sys.path.append(path)
from exception import WrongRectWidth,WrongRectHeight
from rect import Rect
from vector import Vector
from polygone import Polygon
from transformable import Transformable
from transform import Transform
from collideTransformable import CollideTransformable
from hitbox import Hitbox
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_hitbox1():
    T = CollideTransformable()
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    Hb.link(T)
    T.translate(Vector(2,0))
    assert Hb.get_ctrbl().get_position() == Vector(2,0)
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    Hb.link(T)
    T.rotate(np.pi/2) #Isn't supposed to affect hit box (removed in Physics 4.0)
    assert T.get_position() == Vector(2,0)
    T.scale(2,3)
    assert Hb.get_world_rect() == Rect(0,-3,4,6)

    R = Rect(0,0,2,2)
    Hb = Hitbox(R)
    T = CollideTransformable()
    Hb.link(T)
    T.set_position(2,0)
    assert Hb.get_world_rect() == Rect(2,0,2,2)
    T.scale(4,3)
    assert Hb.get_world_rect() == Rect(2,0,8,6)

def test_hitbox2():
    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(-1,-1,2,2)
    R2 = Rect(-1,-1,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    Hb1.link(T1)
    Hb2.link(T2)
    T1.translate(Vector(0.5,0.5))
    assert Hb1.collide(Hb2)
    assert Hb2.collide(Hb1)

    T1.translate(Vector(-0.5,-0.5))
    T2.translate(Vector(2,0))

    assert Hb1.collide(Hb1)
    assert Hb2.collide(Hb2)

    T2.translate(Vector(0.01,0))
    assert not(Hb1.collide(Hb2))
    assert not(Hb2.collide(Hb1))


def test_hitbox3():

    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(-1,-1,2,2)
    R2 = Rect(-1,-1,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    Hb1.link(T1)
    Hb2.link(T2)
    T1.translate(Vector(1,1))
    T2.translate(Vector(2.5,1))
    T1.set_speed(Vector(1,0))
    print(Hb1.get_world_rect())
    print(Hb2.get_world_rect())
    v = Hb1.remove_collide(Hb2)
    print(v)
    T1.translate(v)
    assert not(Hb1.collide(Hb2))

def test_hitbox4():
    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(-1,-1,2,2)
    R2 = Rect(-1,-1,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    Hb1.link(T1)
    Hb2.link(T2)
    T1.translate(Vector(1,1))
    T2.translate(Vector(3,1))
    T2.set_speed(Vector(-1,0))
    v = Hb2.remove_collide(Hb1)
    T2.translate(v)
    assert not(Hb1.collide(Hb2))

"""
def test_hitbox5():
    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(-1,-1,2,2)
    R2 = Rect(-1,-1,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    Hb1.link(T1)
    Hb2.link(T2)
    T1.translate(Vector(1.01,-0.5))
    T2.translate(Vector(2.5,1))
    T1.set_speed(Vector(1,0))
    v = Hb1.remove_collide(Hb2)
    print(v)
    T1.translate(v)
    assert not(Hb1.collide(Hb2))
"""

def test_hitbox6_sides():
    #Test collide_segments for all corners
    
    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(0,0,2,2)
    R2 = Rect(1.5,0,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    T1.set_speed(Vector(1,0))
    T1.set_hit_box(Hb1)
    T2.set_hit_box(Hb2)
    assert Hb1.collide_sides(Hb2) == 3#([1,2],[0,3])

    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(0,0,2,2)
    R2 = Rect(0,1,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    T1.set_speed(Vector(0,1))
    T1.set_hit_box(Hb1)
    T2.set_hit_box(Hb2)
    print(T1.get_hit_box())
    print(T2.get_hit_box())
    assert Hb1.collide_sides(Hb2) == 2 #([0,3],[1,2])

    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(0,0,2,2)
    R2 = Rect(1,-1.5,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    T1.set_hit_box(Hb1)
    T2.set_hit_box(Hb2)
    T1.set_speed(Vector(1,-1))
    assert Hb1.collide_sides(Hb2) == 0 #([0,1],[2,3])

    T1 = CollideTransformable()
    T2 = CollideTransformable()
    R1 = Rect(0,0,2,2)
    R2 = Rect(-1,1.5,2,2)
    Hb1 = Hitbox(R1)
    Hb2 = Hitbox(R2)
    T1.set_hit_box(Hb1)
    T2.set_hit_box(Hb2)
    assert Hb1.collide_sides(Hb2) == 2#([2,3],[0,1])

