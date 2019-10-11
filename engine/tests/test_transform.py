import sys
import os
import numpy as np
path = os.getcwd()
path = path[:-6]
sys.path.append(path)
from transformable import Transform
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_init():
    T = Transform()
    assert T.get_matrix == np.identity()
    T2 = Transform(np.zeros(3,3))
    assert T2.get_matrix == np.zeros((3,3))

def test_inv():
    for i in range(100):
        T = Transform(np.random.rand(3,3))
        assert np.dot(T.get_inverse(),T.get_matrix()) == np.identity

def test_transform_point():
    T = Transform(np.matrix("2 0 0;0 1 0;0 0 1"))
    p1x = 2
    p1y = 3
    assert T.transformPoint(p1x,p1y) == [p1x*2,p1y,1]
    T2 = Transform(np.matrix("1 1 0;1 1 0;0 0 1"))
    p2x = 3
    p2y = 3
    assert T2.transformPoint(p2x,p2y) == [p1x+p1y,p1x+p1y,1]
    T = Transform()
