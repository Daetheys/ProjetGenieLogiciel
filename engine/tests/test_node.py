import sys
import os
sys.path.append(os.getcwd()+"/engine")
from node import Node
from vector import Vector

def test_translation():
    N = Node()
    N2 = Node()
    N.attach_children(N2)
    N.translate(Vector(5,3))
    assert N.get_position() == Vector(5,3)
    assert N2.get_position() == Vector(5,3)

def test_rotation():
    N = Node()
    N2 = Node()
    N2.translate(Vector(5,0))
    N.attach_children(N2)
    N.rot(90)
    assert N2.get_position() == Vector(0,-5)

def test_scale():
    N = Node()
    N2 = Node()
    N.attach_children(N2)
    N.scale(2,2)
    assert N2.get_scale() == Vector(2,2)

def test_rotation1():
    N = Node()
    N2 = Node()
    N2.translate(Vector(5,0))
    N.attach_children(N2)
    N.rot(90)
    assert N2.get_position() == Vector(0,-5)
    assert N2.get_position() == Vector(0,-5)

def test_2_translation():
    N = Node()
    N2 = Node()
    N3 = Node()
    N.attach_children(N2)
    N2.attach_children(N3)
    N.translate(Vector(5,3))
    assert N.get_position() == Vector(5,3)
    assert N2.get_position() == Vector(5,3)
    assert N3.get_position() == Vector(5,3)

def test_2_rotation():
    N = Node()
    N2 = Node()
    N3 = Node()
    N2.translate(Vector(5,0))
    N3.translate(Vector(5,-3))
    N.attach_children(N2)
    N2.attach_children(N3)
    N.rot(90)
    N2.rot(90)
    assert N2.get_position() == Vector(0,-5)
    assert N3.get_position() == Vector(0,-2)

def test_2_rotation_walk():
    N = Node()
    N2 = Node()
    N3 = Node()
    N2.translate(Vector(5,0))
    N3.translate(Vector(5,-3))
    N.attach_children(N2)
    N2.attach_children(N3)
    N.rot(90)
    N2.rot(90)
    for i in range(10):
        print("---")
        N.translate(Vector(1,0))
        assert N2.get_position() == Vector(i+1,-5)
        assert N3.get_position() == Vector(i+1,-2)
