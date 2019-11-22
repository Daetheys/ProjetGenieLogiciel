#!/usr/bin/env python3
import os
import sys
from vector import Vector
from transform import Transform
from polygone import Polygon
path = os.getcwd()
path += "/error"
sys.path.append(path)
from exception import WrongRectWidth,WrongRectHeight

import pygame
import numpy as np
import copy

class Rect:
    """ The Y axis is directed to bottom """
    def __init__(self,left=0,top=0,width=0,height=0):
        if width<0:
            raise WrongRectWidth()
        if height<0:
            raise WrongRectHeight()
        
        self.position = Vector(left,top)
        self.dimension = Vector(width,height)

    def center(self):
        self.set_position(-self.get_dimension()/2)

    def get_coord(self):
        v = self.get_position()
        d = self.get_dimension()
        return (v.x,v.y,d.x,d.y)
        
    def __eq__(self,rect):
        d = self.get_dimension() == rect.get_dimension()
        p = self.get_position() == rect.get_position()
        return d and p

    def __str__(self):
        (l,t,w,h) = self.get_coord()
        return "Rect("+str(l)+","+str(t)+","+str(l+w)+","+str(t+h)+")"

    def rescale(self,alpha):
        self.position *= alpha
        self.dimension *= alpha

    def copy(self):
        """ Returns a copy of this vector """
        (l,t,w,h) = self.get_coord()
        r2 = Rect(l,t,w,h)
        return r2

    def translate(self,v):
        self.set_position(self.get_position()+v)
    
    def init_from_vectors(self,position,dimension):
        self.position = position
        self.dimension = dimension

    def get_points(self):
        return self.get_poly().get_points()

    def get_poly(self):
        (l,t,w,h) = self.get_coord()
        v1 = Vector(l,t)
        v2 = Vector(l+w,t)
        v3 = Vector(l+w,t+h)
        v4 = Vector(l,t+h)
        box = Polygon([v1,v2,v3,v4])
        return box

    def point_in(self,v):
        (l,t,w,h) = self.get_coord()
        min_x=min(l,l+w)
        max_x=max(l,l+w)
        min_y=min(t,h+t)
        max_y=max(t,h+t)
        return (min_x <= v.x <= max_x) and (min_y <= v.y <= max_y)

    def collide_poly(self,poly):
        sfpoly = self.get_poly()
        return sfpoly.collide(poly)
    
    def nearest_wall(self,point):
        (l,t,w,h) = self.get_coord()
        dtop = abs(t - point.y)
        dbot = abs(t+h-point.y)
        dleft = abs(l - point.x)
        dright = abs(l+w-point.x)
        li = [dleft,dtop,dright,dbot]
        index = np.argmin(li)
        return index,li[index]

    def get_position(self):
        return self.position
    
    def get_dimension(self):
        return self.dimension

    def set_position(self,pos):
        self.position = pos

    def set_dimension(self,dim):
        self.dimension = dim

    def to_tuples(self):
        li = []
        for p in self.get_points():
            li.append( (p.x,p.y) )
        return li

    def to_pygame(self):
        (l,t,w,h) = self.get_coord()
        return pygame.Rect(l,t,w,h)
