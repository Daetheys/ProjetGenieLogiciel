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
from collideTransformable import CollideTransformable
from force import Gravity
from rect import Rect
from hitbox import Hitbox
from hypothesis import given
from hypothesis.strategies import integers, lists


@given(integers(min_value=-1000,max_value=1000),integers(min_value=-1000,max_value=1000),integers(min_value=-1000,max_value=1000),integers(min_value=-1000,max_value=1000),integers(min_value=-1000,max_value=1000),integers(min_value=-1000,max_value=1000),integers(min_value=-1000,max_value=1000))
def test_copy(px,py,r,sx,sy,ox,oy):
    """ tests that we can get exactly the set values"""
    T = CollideTransformable()
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
    Hb = Hitbox(Rect(0,0,2,2))
    mvn = CollideTransformable()
    mvn.set_hit_box(Hb)
    mvn.set_rigid_body(True)
    print(mvn.get_position())

    Hb2 = Hitbox(Rect(0,3,2,2))
    mvn2 = CollideTransformable()
    mvn2.set_hit_box(Hb2)
    mvn2.set_rigid_body(True)
    print(mvn.get_position())
    
    mvn.set_speed(Vector(0,4))
    
    assert not(mvn.get_hit_box().collide(mvn2.get_hit_box()))
    
    mvn.move(1)
    
    assert mvn.get_hit_box().collide(mvn2.get_hit_box())
    #assert mvn.get_direction_rigid_collide(p2) == Segment(Vector(-1,3),Vector(1,3))

