from rect import Rect
from polygone import *

import pygame

class Camera:
    def __init__(self):
        self.rect = Rect()
        self.fen = None #Undefined yet

    def set_position(self,pos):
        self.rect.set_position(pos)
        if not(self.fen is None):
            self.compute_distorsion()

    def set_dimension(self,size):
        self.rect.set_dimension(size)
        if not(self.fen is None):
            self.compute_distorsion()

    def get_position(self):
        return self.rect.get_position()

    def get_dimension(self):
        return self.rect.get_dimension()

    def set_fen(self,fen):
        self.fen = fen
        self.compute_distorsion()

    def get_fen(self):
        return self.fen

    def set_distorsion(self,dis):
        self.distorsion = dis

    def get_distorsion(self):
        return self.distorsion

    def compute_distorsion(self):
        (width,height) = (self.fen.get_width(),self.fen.get_height())
        dim = self.get_dimension()
        pos = self.get_position()

        distorsion_scale = Transform().scale(Vector(width/dim.x,height/dim.y))
        distorsion_translate = Transform().translate(-pos)
        self.distorsion = (distorsion_scale,distorsion_translate)
    """
    def compute_distorsion(self):
        (width,height) = (self.fen.get_width(),self.fen.get_height())
        dim = self.get_dimension()
        pos = self.get_position()

        self.distorsion = Transform()
        self.distorsion = self.distorsion.scale(Vector(width/dim.x,height/dim.y))
        self.distorsion = self.distorsion.translate(-pos.copy())#why .copy ??
    """
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

    def flashblack(self):
        v = self.get_dimension()
        pr = pygame.Rect(0,0,self.get_fen().get_width(),self.get_fen().get_height())
        pygame.draw.rect(self.get_fen(),(0,0,0),pr)

    def aff(self,objects):
        if not(self.get_fen() is None):
            self.flashblack()
        for o in objects:
            if self.is_in_camera(o.get_hit_box()):
                o.aff(self.get_fen(),self.get_distorsion())

    def __repr__(self):
        txt = "Camera("+str(self.rect)+")"
        if self.fen is None: txt += "(not init)"
        return txt
