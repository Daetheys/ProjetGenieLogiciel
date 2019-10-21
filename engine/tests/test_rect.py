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
    assert R.contains(2,2)
    assert R.contains(1,1)
    assert R.contains(3,2)
    assert R.contains(2,3)
    assert not(R.contains(4,2))
    assert not(R.contains(3,4))
    assert not(R.contains(1,0))
    assert not(R.contains(0,1))
    assert R.get_position() == Vector(1,1)
    assert R.get_size() == Vector(2,2)
    R2 = Rect(2,2,1,1)
    assert R.intersects(R2)
    R3 = Rect(4,4,2,1)
    assert R.intersects(R3) == None
    assert R2.intersects(R3) == None
    assert R.intersects(R2) == Rect(2,2,1,1)
    R4 = Rect(2,1,2,3)
    assert R.intersects(R4) == Rect(2,1,1,2)
    assert R3.intersects(R4) == None
    try:
        R5 = Rect(0,0,-4,-5)
        assert False
    except WrongRectWidth:
        pass
    try:
        R5 = Rect(0,0,1,-5)
        assert False
    except WrongRectHeight:
        pass
