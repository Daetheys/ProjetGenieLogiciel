from engine.rect import Rect
from engine.transform import Transform
from engine.vector import Vector
from engine.polygone import Polygon,Line,Segment

DEBUG = False

""" Fondamentally a hit box is a rect that has a link to a transformable. It uses its get_transform to compute collisions in its referential or in the real world """

class Hitbox:
    """ Hit box class """
    def __init__(self,rect):
        self.rect = rect #Rect
        self.ctransformable = None #CollideTransformable

    def __repr__(self):
        return "Hitbox("+str(self.get_world_rect())+")"

    def get_rect(self):
        return self.rect

    def get_ctrbl(self):
        """ Get collide transformable associated with this hit box """
        return self.ctransformable

    def set_ctrbl(self,ct):
        """ Set it """
        self.ctransformable = ct

    def link(self,ct):
        """ Alias for set_ctrbl -> easier to remember"""
        self.set_ctrbl(ct)

    def center(self):
        """ Centers the rectangle on (0,0) """
        return self.rect.center()

    def copy(self):
        """ UNLINKED COPY """
        hb = Hitbox(self.rect.copy())
        return hb

    def get_world_rect(self):
        rect = self.rect.copy()
        rect.scale(self.get_ctrbl().get_scale())
        rect.translate(self.get_ctrbl().get_position())
        return rect

    def rescale(self,alpha):
        self.rect.rescale(alpha)

    def collide(self,hb2):
        return self.get_world_rect().intersect(hb2.get_world_rect())

    def collide_sides(self,hb2):
        """ Self is moving against hb2 """
        inter_rect = self.collide(hb2)
        if inter_rect is None:
            return None
        else:
            (w,h) = inter_rect.get_dimension().to_tuple()
            speedf = self.get_ctrbl().get_speed()
            (xi1,yi1,xf1,yf1) = inter_rect.get_tuple()
            (xi2,yi2,xf2,yf2) = self.get_world_rect().get_tuple()
            if w < h: #On prend la val la + orthogonale
                if xi1 == xi2:
                    return 3
                elif xf1 == xf2:
                    return 1
                else:
                    if self.get_ctrbl().get_speed().x > 0:
                        return 3
                    else:
                        return 1
            else:
                if yi1 == yi2:
                    return 0 #Y axis is toward down
                elif yf1 == yf2:
                    return 2
                else:
                    if self.get_ctrbl().get_speed().y > 0:
                        return 2
                    else:
                        return 0

    def remove_collide(self,hb2):
        epsilon = 10**-5
        inter_rect = self.collide(hb2)
        if inter_rect is None:
            return Vector(0,0)
        (w,h) = inter_rect.get_dimension().to_tuple()
        speedf = self.get_ctrbl().get_speed()
        if w < h:
            if speedf.x > 0:
                return Vector(-w-epsilon,0)
            else:
                return Vector(w+epsilon,0)
        else:
            if speedf.y > 0:
                return Vector(0,-h-epsilon)
            else:
                return Vector(0,h+epsilon)
