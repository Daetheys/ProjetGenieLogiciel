from rect import Rect
from polygone import *

import pygame

class Camera:
    """ Camera object """
    def __init__(self):
        self.rect = Rect()
        self.fen = None #Undefined yet

    def set_position(self,pos):
        """ Sets the position of the camera in the GameLevel"""
        self.rect.set_position(pos)
        if not(self.fen is None):
            self.compute_distorsion()

    def set_dimension(self,size):
        """ Set the dimension of the Camera (usefull to zoom) """
        self.rect.set_dimension(size)
        if not(self.fen is None):
            self.compute_distorsion()

    def get_position(self):
        """ Returns the position of the camera """
        return self.rect.get_position()

    def get_dimension(self):
        """ Returns the dimension of the camera """
        return self.rect.get_dimension()

    def set_fen(self,fen):
        """ Set the window in which the camera will output """
        self.fen = fen
        self.compute_distorsion()

    def get_fen(self):
        """ Returns the windows associated with the camera """
        return self.fen

    def set_distorsion(self,dis):
        """ Set the distorsion of the camera (rescale objects and """
        self.distorsion = dis

    def get_distorsion(self):
        """ Returns the distorsion of the camera """
        return self.distorsion

    def compute_distorsion(self):
        """ Computes the distorsion of the camera """
        (width,height) = (self.fen.get_width(),self.fen.get_height())
        dim = self.get_dimension()
        pos = self.get_position()

        distorsion_scale = Transform().scale(Vector(width/dim.x,height/dim.y))
        distorsion_translate = Transform().translate(-pos)
        self.distorsion = (distorsion_scale,distorsion_translate)

    def is_in_camera(self,poly):
        """ Returns true if the polygon is completely in the camera's rect or if it intersects a side """
        r = self.rect.collide_poly(poly)
        return r
    
    def flashblack(self):
        """ Fill the camera with black in order to blit images right after """
        v = self.get_dimension()
        pr = pygame.Rect(0,0,self.get_fen().get_width(),self.get_fen().get_height())
        pygame.draw.rect(self.get_fen(),(0,0,0),pr)

    def aff(self,objects,bg):
        """ Aff all objects that are in the camera """
        if not(self.get_fen() is None):
            self.flashblack()
        bg.show()
        for o in objects:
            if self.is_in_camera(o.get_hit_box().get_world_poly()):
                o.aff(self.get_fen(),self.get_distorsion())

    def __repr__(self):
        txt = "Camera("+str(self.rect)+")"
        if self.fen is None: txt += "(not init)"
        return txt
