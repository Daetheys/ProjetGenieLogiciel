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


@given(integers(),integers(),integers(),integers(),integers(),integers(),integers())
def test_copy(px,py,r,sx,sy,ox,oy):
    """ tests that we can get exactly the set values"""
    T = MovableNode()
    T.set_position(px,py)
    T.set_rotation(r)
    T.set_scale(sx,sy)
    T.set_origin(ox,oy)
    T.set_speed(Vector(2,3))
    T2 = T.copy()
    assert T2.get_position().to_tuple() == (px,py)
    assert T2.get_rotation() == r%(2*np.pi)
    assert T2.get_scale().to_tuple() == (sx,sy)
    assert T2.get_origin().to_tuple() == (ox,oy)
    assert T2.get_speed() == Vector(2,3)
    

def test_direction_rigid_collide():
    v1 = Vector(1,0)
    v2 = Vector(2,1)
    v3 = Vector(1,2)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    mvn = MovableNode()
    mvn.set_hit_box(p)
    mvn.set_rigid_body(True)
    
    v21 = Vector(0,0)
    v22 = Vector(2,0)
    v23 = Vector(2,1)
    v24 = Vector(0,1)
    p2 = Polygon([v21,v22,v23,v24])
    p2.translate(Vector(0,3))
    
    mvn2 = MovableNode()
    mvn2.set_hit_box(p2)
    mvn2.set_rigid_body(True)

    mvn.set_speed(Vector(0,2))
    mvn.move()
    print("mvn",mvn.get_hit_box())
    print("mvn2",mvn2.get_hit_box())
    assert mvn.get_hit_box().collide(mvn2.get_hit_box())
    print(mvn.get_direction_rigid_collide(p2))
    assert mvn.get_direction_rigid_collide(p2) == Segment(Vector(0,3),Vector(2,3))

def test_full_1():
    v1 = Vector(-1,-1)
    v2 = Vector(1,-1)
    v3 = Vector(1,1)
    v4 = Vector(-1,1)
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
    print("mvn",mvn.get_hit_box())
    print("mvn2",mvn2.get_hit_box())
    assert not(mvn.get_hit_box().collide(mvn2.get_hit_box()))
    mvn.move()
    print("mvn af move",mvn.get_hit_box())
    print("mvn2 af move",mvn2.get_hit_box())
    assert mvn.get_hit_box().collide(mvn2.get_hit_box())
    assert mvn.get_direction_rigid_collide(p2) == Segment(Vector(-1,3),Vector(1,3))

