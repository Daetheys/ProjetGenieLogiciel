#!/usr/bin/env python3
import numpy as np
from transform import Transform
from vector import Vector
from polygone import *
import copy

#travis github CI

class Transformable:
    """ Represents a vector """
    def __init__(self):
        self.__origin = Vector(0,0) # Origine du Transformable (CONST for now)
        self.__position = Vector(0,0) # Coordonnees du Transformable dans l'environnement
        self.__rotation = 0 # Rotation actuelle du Transformable
        self.__scale = Vector(1.,1.) # Ecard du transformable
        self.__transform = None # Transformation
        self.__tr_need_up = True # Transformation need update
        self.__inverse_transform = None # Transformation inverse
        self.__inv_tr_need_up = True # Inverse Transformation need update

    def copy(self):
        """ Returns a copy of this vector """
        print("copy trbl")
        t = Transformable()
        self.paste_in(t)
        return t

    def paste_in(self,t):
        vp = self.get_position()
        t.set_position(vp.x,vp.y)
        t.set_rotation(self.get_rotation())
        vs = self.get_scale()
        t.set_scale(vs.x,vs.y)

    def reset_update(self):
        self.__tr_need_up = True
        self.__inv_tr_need_up = True


    def set_position(self,x,y):
        """ Set the positino of this """
        self.__position = Vector(x,y)
        self.reset_update()

    def set_rotation(self,ang):
        """ Set the rotation of this """
        self.__rotation = ang%(2*np.pi) #Il faut que ce soit positif !!
        self.reset_update()

    def set_scale(self,scale_x,scale_y):
        """ Set the scale """
        self.__scale = Vector(scale_x,scale_y)
        self.reset_update()
        
    """
    def set_origin(self,x,y):
        #Don't use it
        self.__origin = Vector(x,y)
        self.reset_update()
    """
    def get_position(self):
        """ Returns the position """
        return self.__position

    def get_rotation(self):
        """ Returns the rotation """
        return self.__rotation

    def get_scale(self):
        """ Returns the scale """
        return self.__scale
    """
    def get_origin(self):
        #Don't use it
        return self.__origin
    """

    def translate(self,v):
        """ Translates this (side effect)"""
        (move_x,move_y) = (v.x,v.y)
        (x,y) = self.__position.x,self.__position.y
        self.set_position(x+move_x,y+move_y)

    def translate2(self,v):
        """ Copies this, translates it and returns the new translated Transformable """
        t2 = self.copy()
        (move_x,move_y) = (v.x,v.y)
        (x,y) = self.__position.x,self.__position.y
        t2.set_position(x+move_x,y+move_y)
        return t2

    def rot(self,angle):
        """ Rotate this with degree """
        self.set_rotation(self.__rotation + angle*np.pi/180)

    def rotate(self,angle):
        """ Rotates this with radian """
        self.set_rotation(self.__rotation+angle)

    def scale(self,scalex,scaley):
        """ Scales this """
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
        assert self.__transform is not None
        return self.__transform
    
    def get_inverse_transform(self):
        #Don't use it
        if self.__inv_tr_need_up:
            self.__inverse_transform = self.get_transform().get_inverse()
            self.__inv_tr_need_up = False
        return self.__inverse_transform

