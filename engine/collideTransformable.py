import numpy as np
from transform import Transform
from vector import Vector
from transformable import Transformable
from hitbox import Hitbox
from rect import Rect
from polygone import *

class CollideTransformable(Transformable):
    def __init__(self):
        super().__init__()
        #-----------------------------
        #         Collisions
        #-----------------------------
        self.__rigid_body = False
        self.__collide = False
        self.__collide_hit_box = Hitbox(Rect(0,0,0,0))
        self.__rigid_hit_box = Hitbox(Rect(0,0,0,0))
        self.rigid_size_factor = 0.999
        #self.center_hit_box()

    def copy(self):
        """ Returns the copy of this with right deep and shallow copies of arguments """
        t = CollideTransformable()
        self.paste_in(t)
        return t

    def center_hit_box(self):
        """ Center its Hitbox """
        tc = self.get_hit_box().center()
        tr = self.get_rigid_hit_box().center()
        assert tr == tc*self.rigid_size_factor
        self.translate(-tc)

    def paste_in(self,t):
        """ Copies this object in t (side effect)"""
        Transformable.paste_in(self,t)
        t.set_collide(self.get_collide())
        t.set_rigid_body(self.get_rigid_body())
        Hb = self.get_hit_box().copy()
        t.set_hit_box(Hb)
        
    def set_rigid_body(self,val):
        """ Sets whether it's a rigid body or not """
        self.__rigid_body = val
        if val:
            self.__collide = True #A rigid body collides

    def get_rigid_body(self):
        """ Returns if it's a rigid body """
        return self.__rigid_body

    def set_collide(self,val):
        """ Sets whether this can collide """
        self.__collide = val

    def get_collide(self):
        """ Returns if this collides """
        return self.__collide

    def set_hit_box(self,val):
        """ Set the collide hit box of this """
        tr = val.center()
        self.__collide_hit_box = val
        self.__collide_hit_box.link(self)
        rigidhb = val.copy()
        rigidhb.rescale(self.rigid_size_factor)
        self.set_rigid_hit_box(rigidhb)
        #assert self.get_rigid_hit_box().get_ctrbl() == self
        self.translate(-tr)

    def get_hit_box(self):
        """ Compute the hit box according to the position / rotation / scale """
        return self.__collide_hit_box

    def set_rigid_hit_box(self,val):
        """ Set the rigid body hit box -- Don't use it if you don't know what you're doing """
        self.__rigid_hit_box = val
        self.__rigid_hit_box.link(self)

    def get_rigid_hit_box(self):
        """ Returns the rigid hit box """
        return self.__rigid_hit_box
