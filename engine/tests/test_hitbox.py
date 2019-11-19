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
from hitbox import Hitbox
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_hitbox1():
    T = Transformable()
    R = Rect(-1,-1,2,2)
    Hb = HitBox(R)
    Hb.link(T)
    T.translate(Vector(2,0))
    assert Hb.get_ctrbl().get_position() == Vector(2,0)
    assert Hb.get_self_poly() == Polygon([Vector(-1,-1),Vector(1,-1),Vector(1,1),Vector(-1,1)])
    assert Hb.get_world_poly() == Polygon([Vector(1,-1),Vector(3,-1),Vector(3,1),Vector(1,1)])
    R = Rect(-1,-1,2,2)
    Hb = HitBox(R)
    Hb.link(T)
    T.rotate(np.pi/2)
    assert T.get_position() == Vector(2,0)
    assert T.get_rotation() == np.pi/2
    assert T.get_transform() == Transform(np.array([[0,-1,2],[1,0,0],[0,0,1]]))
    assert Hb.get_world_poly() == Polygon([Vector(3,-1),Vector(3,1),Vector(1,1),Vector(1,-1)])
    T.scale(2,3)
    print(Hb.get_world_poly())
    assert Hb.get_world_poly() == Polygon([Vector(6,-3),Vector(6,3),Vector(-2,3),Vector(-2,-3)])

def test_hitbox2():
    T1 = Transformable()
    T2 = Transformable()
    R1 = Rect(-1,-1,2,2)
    R2 = Rect(-1,-1,2,2)
    Hb1 = HitBox(R1)
    Hb2 = HitBox(R2)
    Hb1.link(T1)
    Hb2.link(T2)
    T1.translate(Vector(0.5,0.5))
    assert Hb1.points_in(Hb2) == [Vector(-0.5,-0.5)]
    assert Hb2.points_in(Hb1) == [Vector(0.5,0.5)]

    assert Hb1.collide(Hb2)
    assert Hb2.collide(Hb1)

    T1.translate(Vector(-0.5,-0.5))
    T2.translate(Vector(2,0))
    assert Hb1.points_in(Hb2) == [Vector(-1,-1),Vector(-1,1)]
    assert Hb2.points_in(Hb1) == [Vector(1,-1),Vector(1,1)]

    assert Hb1.collide(Hb1)
    assert Hb2.collide(Hb2)

    T2.translate(Vector(0.01,0))
    assert not(Hb1.collide(Hb2))
    assert not(Hb2.collide(Hb1))

    T2.rotate(np.pi/4)
    assert Hb1.collide(Hb2)
    assert Hb2.collide(Hb1)


def test_hitbox3():

    for a in range(3,10):
        print("---a",a)
        T1 = Transformable()
        T2 = Transformable()
        R1 = Rect(-1,-1,2,2)
        R2 = Rect(-1,-1,2,2)
        Hb1 = HitBox(R1)
        Hb2 = HitBox(R2)
        Hb1.link(T1)
        Hb2.link(T2)
        T2.rotate(np.pi/a)
        T1.translate(Vector(1,1))
        T2.translate(Vector(3,1))
        v = Hb1.remove_collide(Hb2)
        T1.translate(v)
        assert not(Hb1.collide(Hb2))


def test_hitbox4():
    for a in range(3,10):
        print("---a",a)
        T1 = Transformable()
        T2 = Transformable()
        R1 = Rect(-1,-1,2,2)
        R2 = Rect(-1,-1,2,2)
        Hb1 = HitBox(R1)
        Hb2 = HitBox(R2)
        Hb1.link(T1)
        Hb2.link(T2)
        T2.rotate(np.pi/a)
        T1.translate(Vector(1,1))
        T2.translate(Vector(3,1))
        v = Hb2.remove_collide(Hb1)
        T2.translate(v)
        assert not(Hb1.collide(Hb2))

def test_hitbox5():

        T1 = Transformable()
        T2 = Transformable()
        R1 = Rect(-1,-1,2,2)
        R2 = Rect(-1,-1,2,2)
        Hb1 = HitBox(R1)
        Hb2 = HitBox(R2)
        Hb1.link(T1)
        Hb2.link(T2)
        T1.translate(Vector(1,-0.5))
        T2.translate(Vector(2.5,1))
        v = Hb1.remove_collide(Hb2)
        T1.translate(v)
        assert not(Hb1.collide(Hb2))

