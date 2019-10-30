#!/usr/bin/env python3
import numpy as np
from transform import Transform
from vector import Vector

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

    def move(self,move_x,move_y):
        (x,y) = self.__position.x,self.__position.y
        self.set_position(x+move_x,y+move_y)

    def rotate(self,angle):
        self.set_rotation(self.__rotation+angle)

    def scale(self,scalex,scaley):
        (x,y) = self.__scale.x,self.__scale.y
        (x2,y2) = (scalex,scaley)
        self.set_scale(x+x2,y+y2)

    def get_transform():
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
            self.__transform = Transform(sxc,sys,tx,-sxs,syc,ty,0,0,1)
            self.__tr_need_up = False
        # Error : returned None at 'get_transform' because the transform_matrix
        # was None and __tr_need_up == False
        assert self.__transform != None
        return self.__transform

    def get_inverse_transform():
        if self.inv_tr_need_up:
            self.__inverse_transform = self.get_transform.get_inverse()
            self.__inv_tr_need_up = False
        return self.__inverse_transform
