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

@given(integers(),integers(),integers(min_value=0),integers(min_value=0))
def test_rect_center_general(x,y,w,h):
    R = Rect(x,y,w,h)
    R.center()
    pos = R.get_position()
    dim = R.get_dimension()
    assert pos.x == -dim.x/2
    assert pos.y == -dim.y/2
