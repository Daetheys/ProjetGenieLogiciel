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
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_gravity():
    movn = CollideTransformable()
    movn.set_mass(5)
    gravity = Gravity(9.81)
    movn.add_force(gravity)
    movn.compute_speed(0.1)
    assert movn.get_acc() == Vector(0,9.81/5)
    assert movn.get_speed() == Vector(0,.981/5)
    movn.move(1)
    print("pos",movn.get_position(),Vector(0,9.81/5))
    assert movn.get_position() == Vector(0,.981/5)
