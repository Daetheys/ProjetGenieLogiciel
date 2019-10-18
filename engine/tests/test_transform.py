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
    T = Transform(np.matrix("2 0 0;0 1 0;0 0 1"))
    p1x = 2
    p1y = 3
    aftertransform = np.array([[p1x*2],[p1y]])
    assert np.allclose(T.transformPoint(p1x,p1y),aftertransform)
    T2 = Transform(np.matrix("1 1 0;1 1 0;0 0 1"))
    p2x = 3
    p2y = 3
    aftertransform = np.array([[p2x+p2y],[p2x+p2y]])
    assert np.allclose(T2.transformPoint(p2x,p2y),aftertransform)

def test_combine():
    T = Transform(np.matrix("2 0 0;1 1 0; 0 0 1"))
    T2 = Transform(np.matrix("1 2 0;0 2 0;0 0 1"))
    Tf = np.matrix("2 4 0;1 4 0;0 0 1")
    Tp = np.dot(T.get_matrix(),T2.get_matrix())
    assert np.allclose(Tp,Tf)

def test_rotate():
    T = Transform(np.matrix("2 0 0;1 1 0;0 0 1"))
    angle0 = np.pi/2
    angle1 = np.pi
    angle2 = 2*np.pi
    T0 = T.rotate(angle0)
    T1 = T.rotate(angle1)
    T2 = T.rotate(angle2)
    M0 = T0.get_matrix()
    M1 = T1.get_matrix()
    M2 = T2.get_matrix()
    S0 = np.matrix("-1 -1 0;2 0 0;0 0 1")
    S1 = np.matrix("-2 0 0;-1 -1 0;0 0 1")
    S2 = np.matrix("2 0 0;1 1 0;0 0 1")
    print(M0)
    assert np.allclose(S0,M0)
    assert np.allclose(S1,M1)
    assert np.allclose(S2,M2)
