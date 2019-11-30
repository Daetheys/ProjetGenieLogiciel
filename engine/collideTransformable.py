import numpy as np
from transform import Transform
from vector import Vector
from transformable import Transformable
from hitbox import Hitbox
from rect import Rect
from polygone import *
from movableNode import MovableNode

""" A collide Transformable is almost the last evolution of this terrifying evolution : it has two hit boxes : a collide one and a rigid one. In fact in pratice because all float computations are approximated it's necessary to have 2 hit boxes, one for collisions (only to say "I collide with you") and an other one for rigid body physics. The rigid body hit box is computed to be a bit smaller than the collide one and to be included in it """


class CollideTransformable(MovableNode):
    def __init__(self):
        super().__init__()
        #-----------------------------
        #         Collisions
        #-----------------------------
        self.__rigid_body = False #Boolean if it's a rigid body
        self.__collide = False #Boolean if it's a collide body
        self.__collide_hit_box = Hitbox(Rect(0,0,0,0)) #Collide hit box (see Hit Box)
        self.__rigid_hit_box = Hitbox(Rect(0,0,0,0)) #Rigid hit box
        self.rigid_size_factor = 0.999 #Scale factor for rigid body hit box

    def copy(self):
        """ Returns the copy of this with right deep and shallow copies of arguments """
        t = CollideTransformable()
        self.paste_in(t)
        return t

    def center_hit_box(self):
        """ Center its Hitbox -> it's very important for the physics"""
        #Centers hit boxes
        tc = self.get_hit_box().center()
        tr = self.get_rigid_hit_box().center()
        #Translates the transformable so that this last operation doesn't affect it's position in the world
        assert tr == tc*self.rigid_size_factor #Verify that rigid_hit_box is included in the collide one
        self.translate(-tc)

    def paste_in(self,t):
        """ Paste this object in t (side effect)"""
        MovableNode.paste_in(self,t)
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
        #Centers the hit box
        tr = val.center()
        #Assign the collide box
        self.__collide_hit_box = val
        self.__collide_hit_box.link(self) #Link the hit box to this collidetransformable (see hitbox)
        #Computes the rigid hit box inside
        rigidhb = val.copy()
        rigidhb.rescale(self.rigid_size_factor)
        self.set_rigid_hit_box(rigidhb)
        #Translates the transformable so that the given hit box stays the same after beeing centered
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

    def apply_solid_reaction(self,support):
        """ Computes physics when this specific node rigid_collides with support"""
        assert self.get_rigid_hit_box().collide(support.get_rigid_hit_box())
        #Get how to remove the collision
        correction = self.get_rigid_hit_box().remove_collide(support.get_rigid_hit_box())
        #Get how to correct the speed
        speed = correction.normalise()*self.get_speed()
        #Correct position and speed
        self.translate(correction)
        self.set_speed(self.get_speed()+speed)
