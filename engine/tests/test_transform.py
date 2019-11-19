import sys
import os
import numpy as np
path = os.getcwd()
path += "/engine"
sys.path.append(path)
from transformable import Transform
from vector import Vector
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_init():
    T = Transform()
    mt = T.get_matrix()
    mi = np.identity(3)
    assert np.array_equal(mt,mi)
    T2 = Transform(np.zeros((3,3)))
    mt2 = T2.get_matrix()
    mz = np.zeros((3,3))
    assert np.array_equal(mt2,mz)

def test_inv():
    for i in range(100):
        T = Transform(np.random.rand(3,3))
        Tinv = T.get_inverse()
        tinvmat = Tinv.get_matrix()
        tmat = T.get_matrix()
        mid = np.identity(3)
        p = np.dot(tinvmat,tmat)
        assert np.allclose(p,mid)

def test_transform_point():
    T = Transform(np.array([[2,0,0],[0,1,0],[0,0,1]]))
    p1x = 2
    p1y = 3
    aftertransform = Vector(p1x*2,p1y)
    assert T.transform_point(p1x,p1y) == aftertransform
    T2 = Transform(np.array([[1,1,0],[1,1,0],[0,0,1]]))
    p2x = 3
    p2y = 3
    aftertransform = Vector(p2x+p2y,p2x+p2y)
    assert T2.transform_point(p2x,p2y) == aftertransform

def test_combine():
    T = Transform(np.array([[2,0,0],[0,1,0],[0,0,1]]))
    T2 = Transform(np.array([[1,1,0],[1,1,0],[0,0,1]]))
    Tf = np.array([[2,2,0],[1,1,0],[0,0,1]])
    Tp = np.dot(T.get_matrix(),T2.get_matrix())
    assert np.allclose(Tp,Tf)

def test_rotate():
    angle0 = np.pi/2
    angle1 = np.pi
    angle2 = 2*np.pi
    T = Transform(np.array([[2,0,0],[0,1,0],[0,0,1]]))
    T0 = T.rotate(-angle0)
    T = Transform(np.array([[2,0,0],[0,1,0],[0,0,1]]))
    T1 = T.rotate(-angle1)
    T = Transform(np.array([[2,0,0],[0,1,0],[0,0,1]]))
    T2 = T.rotate(-angle2)
    M0 = T0.get_matrix()
    M1 = T1.get_matrix()
    M2 = T2.get_matrix()
    S0 = np.array([[0,1,0],[-2,0,0],[0,0,1]])
    S1 = np.array([[-2,0,0],[0,-1,0],[0,0,1]])
    S2 = np.array([[2,0,0],[0,1,0],[0,0,1]])
    print(S0)
    print(M0)
    print("\n")
    assert np.allclose(S0,M0)
    assert np.allclose(S1,M1)
    assert np.allclose(S2,M2)
"""
def test_rotate_around1():
	T = Transform(np.array([[2,0,0],[0,1,0],[0,0,1]]))
	center = Vector(-1.,0.)
	angle = np.pi/2
	T.rotate_around(angle,center)
	S = np.array([[0,2,-2],[-1,0,-1],[0,0,1]])
	assert np.allclose(S,T.get_matrix())

def test_rotate_around2():
	T = Transform(np.array([[2,0,0],[0,1,0],[2,3,1]]))
	center = Vector(-2.,-1.)
	angle = np.pi
	T.rotate_around(angle,center)
	S = np.array([[-2,0,2],[0,-1,3],[0,0,1]])
	assert np.allclose(S,T.get_matrix())
"""
