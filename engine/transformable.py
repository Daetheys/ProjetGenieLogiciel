import numpy as np
from transform import *

#travis github CI

class Transformable:
    def __init__(self):
        self.__origin = (0,0) #Origine du Transformable
        self.__position = (0,0) #Coordonnees du Transformable dans l'environnement
        self.__rotation = 0 #Rotation actuelle du Transformable
        self.__scale = (1,1) #Ecard du transformable
        self.__transform = None #Transformation
        self.__tr_need_up = True #Update Boolean (Transformation need update)
        self.__inverse_transform = None #Transformation inverse
        self.__inv_tr_need_up = True #Update Transformation inverse (Inverse Transformation need update)

    def reset_update(self):
        self.__tr_need_up = True
        self.__inv_tr_need_up = True

    def set_position(self,x,y):
        self.__position = (x,y)
        self.reset_update()

    def set_rotation(self,ang):
        self.__rotation = ang%np.pi #Il faut que ce soit positif !!

    def set_scale(self,scale_x,scale_y):
        self.__scale = (scale_x,scale_y)
        self.reset_update()

    def set_origin(self,x,y):
        self.__origin = (x,y)
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
        (x,y) = self.__position
        self.set_position(x+move_x,y+move_y)

    def rotate(self,angle):
        self.set_rotation(self.__rotation+angle)

    def scale(self,scalex,scaley):
        (x,y) = self.__scale
        (x2,y2) = (scalex,scaley)
        self.set_scale(x+x2,y+y2)

    def get_transform():
        (x,y) = self.__position
        (sx,sy) = self.__scale
        (mx,my) = self.__origin
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
        assert self.__transform != None #Error : returned None at 'get_transform' because the transform_matrix was None and __tr_need_up == False
        return self.__transform

    def get_inverse_transform():
        if self.inv_tr_need_up:
            self.__inverse_transform = self.get_transform.get_inverse()
            self.__inv_tr_need_up = False
        return self.__inverse_transform
