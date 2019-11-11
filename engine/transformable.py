#!/usr/bin/env python3
import numpy as np
from transform import Transform
from vector import Vector
from polygone import *

#travis github CI

class Transformable:
    def __init__(self):
        self.__origin = Vector() # Origine du Transformable
        self.__position = Vector() # Coordonnees du Transformable dans l'environnement
        self.__rotation = 0 # Rotation actuelle du Transformable
        self.__scale = Vector(1.,1.) # Ecard du transformable
        self.__transform = None # Transformation
        self.__tr_need_up = True # Transformation need update
        self.__inverse_transform = None # Transformation inverse
        self.__inv_tr_need_up = True # Inverse Transformation need update

        #-----------------------------
        #         Collisions
        #-----------------------------
        self.__rigid_body = False
        self.__collide = False
        self.__collide_hit_box = Polygon([self.__origin])
        self.__rigid_hit_box = Polygon([self.__origin])

    def set_rigid_body(self,val):
        self.__rigid_body = val
        if val:
            self.__collide = True #A rigid body collides

    def get_rigid_body(self):
        return self.__rigid_body

    def set_collide(self,val):
        self.__collide = val

    def get_collide(self):
        return self.__collide

    def set_hit_box(self,val):
        self.__hit_box = val
        t = Transform().scale(0.99) #0.01% smaller
        self.set_rigid_hit_box(self.get_hit_box().apply_transform(t))

    def get_hit_box(self):
        """ Compute the hit box according to the position / rotation / scale """
        transform = self.get_transform() #Recompute the hit box to avoid comulating errors due to operations on floats that approximate computations
        return self.__hit_box.apply_transform(transform)

    def set_rigid_hit_box(self,val):
        self.__rigid_hit_box = val

    def get_rigid_hit_box(self):
        return self.__rigid_hit_box

    def reset_update(self):
        self.__tr_need_up = True
        self.__inv_tr_need_up = True

    def set_position(self,x,y):
        self.__position = Vector(x,y)
        self.reset_update()

    def set_rotation(self,ang):
        self.__rotation = ang%(2*np.pi) #Il faut que ce soit positif !!

    def set_scale(self,scale_x,scale_y):
        self.__scale = Vector(scale_x,scale_y)
        self.reset_update()

    def set_origin(self,x,y):
        self.__origin = Vector(x,y)
        self.reset_update()

    def get_position(self):
        return self.__position

    def get_rotation(self):
        return self.__rotation

    def get_scale(self):
        return self.__scale

    def get_origin(self):
        return self.__origin

    def translate(self,v):
        (move_x,move_y) = (v.x,v.y)
        (x,y) = self.__position.x,self.__position.y
        self.set_position(x+move_x,y+move_y)

    def rotate(self,angle):
        self.set_rotation(self.__rotation+angle)

    def scale(self,scalex,scaley):
        (x,y) = self.__scale.x,self.__scale.y
        (x2,y2) = (scalex,scaley)
        self.set_scale(x+x2,y+y2)

    def get_transform(self):
        (x,y) = self.__position.x,self.__position.y
        (sx,sy) = self.__scale.x,self.__scale.y
        (mx,my) = self.__origin.x,self.__origin.y
        if self.__tr_need_up:
            angle = -self.__rotation
            cosine = np.cos(angle)
            sine = np.sin(angle)
            sxc = sx*cosine
            syc = sy*cosine
            sxs = sx*sine
            sys = sy*sine
            tx = -mx*sxc - my*sys + x
            ty =  mx*sxs - my*syc + y
            self.__transform = Transform(np.array([[sxc,sys,tx],[-sxs,syc,ty],[0,0,1]]))
            self.__tr_need_up = False
        # Error : returned None at 'get_transform' because the transform_matrix
        # was None and __tr_need_up == False
        assert self.__transform != None
        return self.__transform

    def get_inverse_transform(self):
        if self.__inv_tr_need_up:
            self.__inverse_transform = self.get_transform().get_inverse()
            self.__inv_tr_need_up = False
        return self.__inverse_transform

