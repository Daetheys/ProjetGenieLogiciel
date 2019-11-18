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
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_rect1():
    R = Rect(1,1,2,2)
    assert R.point_in(Vector(2,2))
    assert R.point_in(Vector(1,1))
    assert R.point_in(Vector(3,2))
    assert R.point_in(Vector(2,3))
    assert not(R.point_in(Vector(4,2)))
    assert not(R.point_in(Vector(3,4)))
    assert not(R.point_in(Vector(1,0)))
    assert not(R.point_in(Vector(0,1)))
    assert R.get_position() == Vector(1,1)
    assert R.get_dimension() == Vector(2,2)

def test_rect2():
    R = Rect(-1,-1,2,2)
    R.translate(Vector(2,0))
    assert R.get_box().get_points() == [Vector(1,-1),Vector(3,-1),Vector(3,1),Vector(1,1)]
    R = Rect(-1,-1,2,2)
    R.rotate(np.pi/2)
    assert R.get_box().get_points() == [Vector(-1,1),Vector(-1,-1),Vector(1,-1),Vector(1,1)]
    R.scale(Vector(2,2))
    assert (R.get_box()/2).get_points() == [Vector(-1,1),Vector(-1,-1),Vector(1,-1),Vector(1,1)]

def test_rect3():
    R1 = Rect(-1,-1,2,2)
    R2 = Rect(0.5,0,2,2)
    print(R1.points_in(R2))
    assert R1.points_in(R2) == [Vector(1,1)]
    assert R2.points_in(R1) == [Vector(0.5,0)]

    assert R1.collide(R2)
    assert R2.collide(R1)

    R3 = Rect(-1,-1,2,2)
    R4 = Rect(1,-1,2,2)
    assert R3.points_in(R4) == [Vector(1,-1),Vector(1,1)]
    assert R4.points_in(R3) == [Vector(1,-1),Vector(1,1)]

    assert R3.collide(R4)
    assert R4.collide(R4)

    R5 = Rect(-1,-1,2,2)
    R6 = Rect(1.01,-1,2,2)
    assert not(R5.collide(R6))
    assert not(R6.collide(R5))

    R6.rotate(np.pi/4)
    assert R5.collide(R6)
    assert R6.collide(R5)

def test_rec4():

    for a in range(3,10):
        print("---a",a)
        R1 = Rect(-1,-1,2,2)
        R2 = Rect(-1,-1,2,2)
        R2.rotate(np.pi/a)
        R1.translate(Vector(1,1))
        R2.translate(Vector(3,1))
        print("RR2",R2.get_box())
        v = R1.remove_collide(R2)
        R1.translate(v)
        print(v)
        print(R1.get_box())
        print(R2.get_box())
        assert not(R1.collide(R2))

def test_rec5():
    for a in range(4,10):
        print("---a",a)
        R1 = Rect(-1,-1,2,2)
        R2 = Rect(-1,-1,2,2)
        R2.rotate(np.pi/a)
        R1.translate(Vector(1,1))
        R2.translate(Vector(3,1))
        print("RR2",R2.get_box())
        v = R2.remove_collide(R1)
        R2.translate(v)
        print(v)
        print(R1.get_box())
        print(R2.get_box())
        assert not(R1.collide(R2))

def test_rec6():

        R1 = Rect(-1,-1,2,2)
        R2 = Rect(-1,-1,2,2)
        R1.translate(Vector(1,-0.5))
        R2.translate(Vector(2.5,1))
        print("RR2",R2.get_box())
        v = R1.remove_collide(R2)
        R1.translate(v)
        print(v)
        print(R1.get_box())
        print(R2.get_box())
        assert not(R1.collide(R2))
