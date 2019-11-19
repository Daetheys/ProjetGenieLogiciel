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
from rect import Rect
from hitbox import Hitbox
from hypothesis import given
from hypothesis.strategies import integers, lists


@given(integers(),integers(),integers(),integers(),integers(),integers(),integers())
def test_copy(px,py,r,sx,sy,ox,oy):
    """ tests that we can get exactly the set values"""
    T = MovableNode()
    T.set_position(px,py)
    T.set_rotation(r)
    T.set_scale(sx,sy)
    #T.set_origin(ox,oy)
    T.set_speed(Vector(2,3))
    T2 = T.copy()
    print(T2.get_scale(),T.get_scale())
    T.set_position(0,0)
    T.set_rotation(0)
    T.set_scale(0,0)
    T.set_speed(Vector(0,0))
    assert T2.get_position().to_tuple() == (px,py)
    assert T2.get_rotation() == r%(2*np.pi)
    assert T2.get_scale().to_tuple() == (sx,sy)
    #assert T2.get_origin().to_tuple() == (ox,oy)
    assert T2.get_speed() == Vector(2,3)
    


def test_full_1():
    v1 = Vector(-1,-1)
    v2 = Vector(1,-1)
    v3 = Vector(1,1)
    v4 = Vector(-1,1)
    Hb = Hitbox(Rect(-1,-1,2,2))
    mvn = MovableNode()
    mvn.set_hit_box(Hb)
    mvn.set_rigid_body(True)

    mvn2 = mvn.copy()
    
    mvn.translate(Vector(0.001,4))
    mvn.set_speed(Vector(0,-4))
    
    assert not(mvn.get_hit_box().collide(mvn2.get_hit_box()))
    
    mvn.move()
    
    assert mvn.get_hit_box().collide(mvn2.get_hit_box())
    #assert mvn.get_direction_rigid_collide(p2) == Segment(Vector(-1,3),Vector(1,3))

