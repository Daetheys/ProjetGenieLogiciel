from rect import Rect
from polygone import *

import sys
import os
path = os.getcwd()
sys.path.append(path + "/engine")
sys.path.append(path + "/game")

import tools
import pygame

""" A Camera object that represents what will be shown to the player. It uses a Rect (cf Rect) to define what is inside the view of the camera and then rescales and translates things so that they fit exactly in the window (it's the distorsion). This distorsion is a couple of Transform : (tr_scale,tr_translate) """

class Camera:
    """ Camera object """
    def __init__(self):
        self.rect = Rect()
        self.fen = None #Undefined yet

    def move(self,v):
        """ Moves the camera """
        self.rect.translate(v)

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

    def center_on(self,pos):
        """ Centers the camera on a position """
        pos = pos
        pos = pos + (-self.get_dimension()/2)
        self.set_position(pos)

    def threeforth_on(self,pos):
        """ Makes a 3/4 on the position (this position will be on the left and 3/4 of the screen is free on the right -> usefull for a Canabalt style game """
        dim = self.get_dimension()
        pos += (-Vector(dim.x/4,dim.y/2))
        self.set_position(pos)
    
    def flashblack(self):
        """ Fill the camera with black in order to blit images right after """
        v = self.get_dimension()
        pr = pygame.Rect(0,0,self.get_fen().get_width(),self.get_fen().get_height())
        pygame.draw.rect(self.get_fen(),(0,0,0),pr)

    def aff(self,objects,bg,score):
        """ Show all objects of the given argument that are in the camera as well as the background and the score """
        #Starts with a flashblack
        if not(self.get_fen() is None):
            self.flashblack()
        #Shows the Bakcground (see Background)
        bg.show()
        #Shows all objects that are in the camera
        for o in objects:
            if self.is_in_camera(o.get_hit_box().get_world_poly()): #Checks if the hitbox is in the camera
                o.aff(self.get_fen(),self.get_distorsion())
        #Show the score
        d = self.get_dimension()
        x = int(d.x*15/16) #Computes where to put it
        y = int(d.y*1/16)
        distorsion_scale = self.get_distorsion()[0]
        vpos = distorsion_scale.transform_point(x,y)
        tools.T(self.get_fen(),str(score),vpos.x,vpos.y,255,255,255,size=45)

    def __repr__(self):
        txt = "Camera("+str(self.rect)+")"
        if self.fen is None: txt += "(not init)"
        return txt
