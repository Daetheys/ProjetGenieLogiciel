import sys
import os
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from hypothesis import given
from hypothesis.strategies import integers, lists, tuples

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
    s4 = Segment(Vector(0,0),Vector(0,1))
    s5 = Segment(Vector(0,-1),Vector(0,2))
    assert s4.collide_segment(s5)
    s6 = Segment(Vector(0,2),Vector(2,2))
    s7 = Segment(Vector(-1,2),Vector(1,2))
    assert s6.collide_segment(s7)
    s6 = Segment(Vector(0,2),Vector(2,2))
    s7 = Segment(Vector(-1,2),Vector(1,2))
    assert s6.collide_segment(s7)

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
    assert not(p.point_in(Vector(1.2,0.1)))

def test_polygone_point_in2():
    v1 = Vector(1,0)
    v2 = Vector(2,1)
    v3 = Vector(1,2)
    v4 = Vector(0,1)
    p = Polygon([v1,v2,v3,v4])
    assert p.point_in(Vector(1,1))
    assert not(p.point_in(Vector(2,2)))
    assert p.point_in(Vector(0.5,1))
    assert p.point_in(Vector((3**0.5)/2+0.001,(3**0.5)/2+0.001))
    assert p.point_in(Vector(0.7,1.1))

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

def test_polygon_apply_transform():
    v1 = Vector(-1,-1)
    v2 = Vector(2,-1)
    v3 = Vector(2,2)
    v4 = Vector(-1,2)
    p = Polygon([v1,v2,v3,v4])
    t = Transform()
    t.rotate(-3*np.pi/2)
    pat = p.apply_transform(t)
    v21 = Vector(1,-1)
    v22 = Vector(1,2)
    v23 = Vector(-2,2)
    v24 = Vector(-2,-1)
    p2 = Polygon([v21,v22,v23,v24])
    assert pat == p2

def test_polygon_max_min():
    v1 = Vector(0,3)
    v2 = Vector(4,5)
    v3 = Vector(0,8)
    p = Polygon([v1,v2,v3])
    assert p.get_max_x() == 4
    assert p.get_max_y() == 8
    assert p.get_min_x() == 0
    assert p.get_min_y() == 3

def test_more1():
    v1 = Vector(1,6)
    v2 = Vector(1,5)
    v3 = Vector(3,5)
    v4 = Vector(3,6)
    p1 = Polygon([v1,v2,v3,v4])

    v21 = Vector(7,5)
    v22 = Vector(7,4)
    v23 = Vector(9,4)
    v24 = Vector(9,5)
    p2 = Polygon([v21,v22,v23,v24])

    assert not(p1.collide(p2))

def test_more2():
    p1 = Polygon([Vector(-2.0,6.0), Vector(2.0,6.0), Vector(2.0,10.0), Vector(-2.0,10.0)])
    p2 = Polygon([Vector(-1.0,1.999969482421875), Vector(3.0,1.999969482421875), Vector(3.0,5.999969482421875), Vector(-1.0,5.999969482421875)])

    assert p1.points_in(p2) == []

def test_more3():
    p1 = Polygon([Vector(-1.0,-1.0), Vector(1.0,-1.0), Vector(1.0,1.0), Vector(-1.0,1.0)])
    p2 = Polygon([Vector(-1.0,3.0), Vector(1.0,3.0), Vector(1.0,5.0), Vector(-1.0,5.0)])
    assert not(p1.collide(p2))


# ----------------------
#
#       BIG TESTS
#
# ----------------------
VALUE = 10**5

@given(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE))
def test_big_line_inter(a,b,a2,b2):
    l = Line(a,b)
    l2 = Line(a2,b2)
    inter_p = l.intersect_point(l2)
    if inter_p is None:
        assert a == a2 and b != b2
    elif isinstance(inter_p,Line):
        assert a == a2 and b == b2
    else:
        assert np.isclose(a*inter_p.x+b,a2*inter_p.x+b2)
        assert np.isclose(a*inter_p.x+b,inter_p.y)

@given(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE))
def test_big_line_inter2(a,b,x):
    l = Line(a,b)
    l2 = Line(0,0,True,x)
    inter_p1 = l.intersect_point(l2)
    inter_p2 = l2.intersect_point(l)
    assert np.isclose(inter_p1.x,x)
    assert np.isclose(a*inter_p1.x+b,inter_p1.y)

    assert np.isclose(inter_p2.x,x)
    assert np.isclose(a*inter_p2.x+b,inter_p2.y)

@given(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE))
def test_big_line_inter3(x,x2):
    l = Line(0,0,True,x)
    l2 = Line(0,0,True,x2)
    inter_p = l.intersect_point(l2)
    if isinstance(inter_p,Line):
        assert np.isclose(x,x2)
    else:
        assert inter_p is None
        assert x != x2
"""
@given(tuples(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE)),tuples(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE)),tuples(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE)),tuples(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE)))
def test_big_segments(p11,p12,p21,p22):
    if not(p11 == p12 or p21 == p22):
        (x11,y11) = p11
        (x12,y12) = p12
        (x21,y21) = p21
        (x22,y22) = p22
        s1 = Segment(Vector(x11,y11),Vector(x12,y12))
        s2 = Segment(Vector(x21,y21),Vector(x22,y22))
        v1 = s1.get_inter_segment(s2)
        v2 = s2.get_inter_segment(s1)
        print("inter",v1,v2)
        assert (v1 == v2)
        if not(v1 is None):
            if not(isinstance(v1,Line)):
                assert s1.contains(v1)
                assert s2.contains(v1)
"""
@given(lists(tuples(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE))),tuples(integers(min_value=-VALUE,max_value=VALUE),integers(min_value=-VALUE,max_value=VALUE)))
def test_big_is_in_poly(l,pt):
    if len(l) > 3:
        lv = []
        for (x,y) in l:
            v = Vector(x,y)
            if not(v in lv):
                lv.append(v)
        p = Polygon(lv)
        pt = Vector(pt[0],pt[1])
        b = p.point_in(pt)
        if b:
            assert p.min_x <= pt.x <= p.max_x
            assert p.min_y <= pt.y <= p.max_y
