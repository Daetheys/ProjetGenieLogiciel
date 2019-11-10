import sys
import os
import numpy as np
import copy as copy

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform
from gameLevel import GameLevel
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_size_level():
    v1 = Vector(0,0)
    v2 = Vector(1,0)
    v3 = Vector(1,1)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    plat1 = SolidPlatform(p)
    p2 = copy.copy(p)
    p2.translate(Vector(3,2))
    plat2 = SolidPlatform(p2)
    gl = GameLevel([plat1,plat2])
    assert gl.size_level == (0,4,0,3)
