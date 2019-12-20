import sys
import os
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform


v1 = Vector(0,0)
v2 = Vector(2,1)
s = Segment(v1,v2)
vs = s.get_vector()
ls1 = s.get_line()

v = Vector(1,2)

v1 += v
v2 += v

s2 = Segment(v1,v2)

ls2 = s2.get_line()

print(ls1,ls2)
print(v.y-v.x*vs.y/vs.x)


