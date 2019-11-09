import sys
import os
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from hypothesis import given
from hypothesis.strategies import integers, lists

def test_line_point_up():
    l1 = Line(1,1)
    assert l1.is_point_up(Vector(0,2))
    assert not(l1.is_point_up(Vector(0,0)))
    assert l1.is_point_up(Vector(1,2))
    l2 = Line(0,0,True,3)
    assert l2.is_point_up(Vector(3,2))
    assert l2.is_point_up(Vector(3,-5))
    assert not(l2.is_point_up(Vector(2,5)))
    assert not(l2.is_point_up(Vector(4,3)))
    l3 = Line(1,2)
    assert not(l3.is_point_up(Vector(1,1)))
    assert not(l3.is_point_up(Vector(2,3)))

#Discretisation pb when testing (too high values are a problem)

def cut(v):
    if abs(v)>10**5:
        if v > 0:
            return 10**5
        else:
            return -10**5
    return v
        
@given(integers(),integers(),integers(),integers())
def test_inter_point(a1,b1,a2,b2):
    a1 = cut(a1)
    a2 = cut(a2)
    b1 = cut(b1)
    b2 = cut(b2)
    if not(a1 == b1 and b1 == 0 or a2 == b2 and b2 == 0):
        l1 = Line(a1,b1)
        l2 = Line(a2,b2)
        p = l1.intersect_point(l2)
        if p is None:
            assert a1 == a2
        else:
            assert np.isclose(l2.a*p.x + l2.b,l1.a*p.x + l1.b)

def test_segment_collide_line():
    s = Segment(Vector(1,1),Vector(2,3))
    l = Line(1,2)
    assert not(s.collide_line(l))
    s2 = Segment(Vector(2,4),Vector(8,7))
    l2 = Line(1,0)
    assert s2.collide_line(l2)

def test_segment_collide_segment():
    s1 = Segment(Vector(1,1),Vector(1,2))
    s2 = Segment(Vector(2,2),Vector(0,2))
    assert s1.collide_segment(s2)
    s3 = Segment(Vector(0,0),Vector(0,2))
    s4 = Segment(Vector(-0.5,0.5),Vector(0.5,0.5))
    assert s4.collide_segment(s3)

def test_is_in_interval_x():
    s1 = Segment(Vector(-1,1),Vector(2,1))
    assert s1.is_in_interval_x(0)
    assert s1.is_in_interval_x(-1)
    assert s1.is_in_interval_x(0.5)
    assert not(s1.is_in_interval_x(3))

def test_len():
    s1 = Segment(Vector(-1,1),Vector(2,1))
    assert s1.length() == 3
    s2 = Segment(Vector(1,2),Vector(3,2))
    assert s2.length() == 2
    s3 = Segment(Vector(2,2),Vector(1,1))
    assert s3.length() == 2**0.5

def test_get_line():
    s1 = Segment(Vector(1,1),Vector(2,2))
    assert s1.get_line() == Line(1,0)
    s2 = Segment(Vector(2,1),Vector(2,2))
    assert s2.get_line() == Line(0,0,True,2)
    s3 = Segment(Vector(-1,1),Vector(2,7))
    assert s3.get_line() == Line(2,3)

def test_polygon_segments():
    v1 = Vector(1,1)
    v2 = Vector(2,3)
    v3 = Vector(4,5)
    p1 = Polygon([v1,v2,v3])
    p1.compute_segments()
    assert p1.get_segments() == [Segment(v1,v2),Segment(v2,v3),Segment(v3,v1)]

def test_polygone_translate():
    v1 = Vector(2,0)
    v2 = Vector(4,0)
    v3 = Vector(1,1)
    v4 = Vector(1,0)
    p = Polygon([v1,v2,v3,v4])
    p.compute_segments()
    p.translate(Vector(-1,1))
    vv1 = Vector(1,1)
    vv2 = Vector(3,1)
    vv3 = Vector(0,2)
    vv4 = Vector(0,1)
    assert p.get_points() == [vv1,vv2,vv3,vv4]
    assert p.get_segments() == [Segment(vv1,vv2),Segment(vv2,vv3),Segment(vv3,vv4),Segment(vv4,vv1)]

def test_polygone_point_in():
    v1 = Vector(0,0)
    v2 = Vector(1,0)
    v3 = Vector(1,1)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    assert p.point_in(Vector(0.5,0.3))
    assert p.point_in(Vector(1,1))
    assert not(p.point_in(Vector(1.2,0)))

def test_polygon_intersect_segment():
    v1 = Vector(0,0)
    v2 = Vector(2,0)
    v3 = Vector(2,2)
    v4 = Vector(0,2)
    p = Polygon([v1,v2,v3,v4])
    s1 = Segment(Vector(1,1),Vector(2,2))
    s2 = Segment(Vector(-0.5,0.5),Vector(0.5,0.5))
    assert p.intersect_segment(s1)
    assert p.intersect_segment(s2)
    s3 = Segment(Vector(2.001,2),Vector(3,3))
    assert not(p.intersect_segment(s3))
