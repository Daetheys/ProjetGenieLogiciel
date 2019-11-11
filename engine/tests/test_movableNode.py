import sys
import os
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from movableNode import MovableNode
from force import Gravity
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_object_collide_reaction():
    v1 = Vector(0,0)
    v2 = Vector(1,0)
    v3 = Vector(1,1)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    mvn = MovableNode()
    mvn.set_hit_box(p)
    mvn.set_rigid_body(True)
    p2 = p.copy()
    t = Transform()
    p2.translate(Vector(0,4))
    mvn2 = MovableNode()
    mvn2.set_hit_box(p2)
    mvn2.set_rigid_body(True)
    mvn.set_speed(Vector(0,4))
    assert not(mvn.get_hit_box().collide(mvn2.get_hit_box()))
    mvn.move()
    assert mvn.get_hit_box().collide(mvn2.get_hit_box())
    assert mvn.get_object_collide(p2) == Segment(Vector(0,4),Vector(1,4))
    v = mvn.get_resistance_support(mvn2)
    mvn.apply_reaction(mvn2)
    assert mvn.get_speed() == Vector(0,0)
