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
    assert T.get_matrix == np.identity
    T2 = Transform(np.zeros(-3,3))
