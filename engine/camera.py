from rect import Rect
from polygone import *

class Camera:
    def __init__(self):
        self.rect = Rect()

    def set_position(self,pos):
        self.rect.set_position(pos)

    def set_dimension(self,size):
        self.rect.set_dimension(size)

    def get_position(self):
        return self.rect.get_position()

    def get_dimension(self):
        return self.rect.get_dimension()

    def is_in_camera(self,polygon):
        """ Returns true if the polygon is completely in the camera's rect or if it intersects a side """
        f_in = True
        for p in polygon.get_points():
            if not(self.rect.contains_vect(p)):
                f_in = False
        rv = self.rect.get_position()
        (rx,ry) = (rv.x,rv.y)
        sv = self.rect.get_dimension()
        (sx,sy) = (sv.x,sv.y)
        tl = Vector(rx,ry)
        bl = Vector(rx,ry+sy)
        tr = Vector(rx+sx,ry)
        br = Vector(rx+sx,ry+sy)
        left_seg = Segment(tl,bl)
        top_seg = Segment(tl,tr)
        right_seg = Segment(tr,br)
        bot_seg = Segment(bl,br)
        f_sides = False
        for side in [left_seg,top_seg,right_seg,bot_seg]:
            f_sides = f_sides or polygon.intersect_segment(side)
        return f_in or f_sides

    def __repr__(self):
        return "Camera("+str(self.rect)+")"
