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

def test_rect_center():
    R = Rect(0,0,2,2)
    tr = R.center()
    assert R == Rect(-1,-1,2,2)
    assert tr == Vector(-1,-1)
    R2 = Rect(-2,-2,2,2)
    tr2 = R2.center()
    assert R2 == Rect(-1,-1,2,2)
    assert tr2 == Vector(1,1)

def test_rect_intersect():
    R1 = Rect(-1,-1,2,2)
    R2 = Rect(0,0,2,2)
    assert R1.intersect(R2) == Rect(0,0,1,1)

    R1 = Rect(-1,-1,2,2)
    R2 = Rect(0,0,1,1)
    assert R1.intersect(R2) == Rect(0,0,1,1)

    R1 = Rect(-3,-3,2,2)
    R2 = Rect(0,0,2,2)
    assert R1.intersect(R2) is None

def test_collidex():
    R1 = Rect(0,0,2,0.1)
    R2 = Rect(1,1,1,1)
    assert R1.collidex(R2)
    R1 = Rect(0,0,2,1)
    R2 = Rect(3,0,1,1)
    assert not(R1.collidex(R2))
    R1 = Rect(0,0,2,2)
    R2 = Rect(2,1,3,3)
    assert R1.collidex(R2)

@given(integers(),integers(),integers(min_value=0),integers(min_value=0))
def test_rect_center_general(x,y,w,h):
    R = Rect(x,y,w,h)
    R.center()
    pos = R.get_position()
    dim = R.get_dimension()
    assert pos.x == -dim.x/2
    assert pos.y == -dim.y/2
