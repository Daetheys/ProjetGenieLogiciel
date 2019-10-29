import sys
import os
import numpy as np

assert False
path = os.getcwd()
path += "/engine"
sys.path.append(path)
from transformable import Transformable
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_rotten_green():
    pass

def test_init():
    T = Transformable()
    assert T.get_position().to_tuple() == (0,0)
    assert T.get_rotation() == 0
    assert T.get_scale().to_tuple() == (1,1)
    assert T.get_origin().to_tuple() == (0,0)

@given(integers(),integers(),integers(),integers(),integers(),integers(),integers())
def test_set_get(px,py,r,sx,sy,ox,oy):
    T = Transformable()
    T.set_position(px,py)
    T.set_rotation(r)
    T.set_scale(sx,sy)
    T.set_origin(ox,oy)
    assert T.get_position().to_tuple() == (px,py)
    assert T.get_rotation() == r%np.pi
    assert T.get_scale().to_tuple() == (sx,sy)
    assert T.get_origin().to_tuple() == (ox,oy)
    
@given(integers(),integers(),integers(),integers(),integers())
def test_move_rot_scal(mvx,mvy,rot,scalx,scaly):
    T = Transformable()
    T.move(mvx,mvy)
    T.rotate(rot)
    T.scale(scalx,scaly)
    assert T.get_position().to_tuple() == (0+mvx,0+mvy)
    assert T.get_rotation() == (0+rot)%np.pi
    assert T.get_scale().to_tuple() == (1.+scalx,1.+scaly)
