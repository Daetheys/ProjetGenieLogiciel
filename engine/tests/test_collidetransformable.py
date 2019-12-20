import sys
import os
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from transformable import Transformable
from vector import Vector
from collideTransformable import CollideTransformable
from rect import Rect
from hitbox import Hitbox
from polygone import Polygon

def test_copy():
    r = Rect(-1,-1,2,2)
    Hb = Hitbox(r)
    t = CollideTransformable()
    t.set_hit_box(Hb)
    t.set_collide(True)
    t2 = t.copy()
    t.set_collide(False)
    assert t2.get_collide()
    Hb2 = t2.get_hit_box()
    assert Hb2.get_ctrbl() == t2
    t2.translate(Vector(2,0))
    assert Hb2.get_world_rect() == Rect(1,-1,2,2)
    assert Hb.get_world_rect() == Rect(-1,-1,2,2)

def test_center():
    r = Rect(0,0,2,2)
    Hb = Hitbox(r)
    t = CollideTransformable()
    t.set_hit_box(Hb)
    assert t.get_hit_box().get_world_rect() == Rect(0,0,2,2)
    assert t.get_position() == Vector(1,1)


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

