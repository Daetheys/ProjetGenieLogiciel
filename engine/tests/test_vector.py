from hypothesis import given
from hypothesis.strategies import integers, lists
import numpy as np
import sys
import os
sys.path.append(os.getcwd()+"/engine")
from vector import Vector

@given(integers(),integers())
def test_vector_base(x,y):
	v = Vector(x,y)
	assert v.x == x
	assert v.y == y

@given(integers(),integers())
def test_vector_homogeneous(x,y):
	v = Vector(x,y)
	assert np.array_equal(v.homogeneous(),np.array([[x],[y],[1]]))

def test_rotate_around():
        v2 = Vector(1,1)
        assert v2.rotate2(np.pi/2) == Vector(1,-1)
        assert v2.rotate2(np.pi) == Vector(-1,-1)
