#!/usr/bin/env python3

from engine.vector import Vector
from engine.transform import Transform
from engine.polygone import Polygon

from error.exception import WrongRectWidth,WrongRectHeight

import pygame
import numpy as np
import copy

""" Rect class : geometry of rectangle """

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
        """ Centers the rectangle on (0,0) """
        pos = self.get_position()
        self.set_position(-self.get_dimension()/2)
        return (self.get_position()+(-pos))

    def collidex(self,orect):
        (oix,oiy,ofx,ofy) = orect.get_tuple()
        (cix,ciy,cfx,cfy) = self.get_tuple()
        return oix<=cix<=ofx or cix<=oix<=cfx or oix<=cfx<=ofx or cix<=ofx<=cfx

    def dist(self,orect):
        (oix,oiy,ofx,ofy) = orect.get_tuple()
        (cix,ciy,cfx,cfy) = self.get_tuple()
        xc1,xc2 = (ofx-oix)/2,(cfx-cix)/2
        yc1,yc2 = (ofy-oiy)/2,(cfy-ciy)/2
        return ((xc1-xc2)**2+(yc1-yc2)**2)**0.5

    def radius(self):
        (cix,ciy,cfx,cfy) = self.get_tuple()
        xc,yc = (cfx-cix)/2,(cfy-ciy)/2
        return ((xc-cix)**2+(yc-ciy)**2)**0.5
                
    def get_coord(self):
        """ Return a 4-tuple of (posx,posy,width,height) """
        v = self.get_position()
        d = self.get_dimension()
        return (v.x,v.y,d.x,d.y)

    def get_tuple(self):
        """ Return a 4-tuple of (posix,posiy,posfx,posfy) """
        v = self.get_position()
        d = self.get_dimension()
        return (v.x,v.y,v.x+d.x,v.y+d.y)

    def __eq__(self,rect):
        d = self.get_dimension() == rect.get_dimension()
        p = self.get_position() == rect.get_position()
        return d and p

    def __repr__(self):
        (l,t,w,h) = self.get_coord()
        return "Rect("+str(l)+","+str(t)+","+str(w)+","+str(h)+")"

    def intersect(self,r2):
        (x1i,y1i) = self.get_position().to_tuple()
        (x1f,y1f) = (self.get_position()+self.get_dimension()).to_tuple()
        (x2i,y2i) = r2.get_position().to_tuple()
        (x2f,y2f) = (r2.get_position()+r2.get_dimension()).to_tuple()
        xi = max(x1i,x2i)
        yi = max(y1i,y2i)
        xf = min(x1f,x2f)
        yf = min(y1f,y2f)
        if xf - xi < 0 or yf-yi < 0:
            return None
        return Rect(xi,yi,xf-xi,yf-yi)


    def rescale(self,alpha):
        """ Rescale """
        self.position *= alpha
        self.dimension *= alpha

    def scale(self,scale):
        self.position *= scale
        self.dimension *= scale

    def scale2(self,scale):
        r2 = self.copy()
        r2.position *= scale
        r2.dimension *= scale
        return r2

    def copy(self):
        """ Returns a copy of this vector """
        (l,t,w,h) = self.get_coord()
        r2 = Rect(l,t,w,h)
        return r2

    def translate(self,v):
        """ Translate with side effect """
        self.set_position(self.get_position()+v)

    def translate2(self,v):
        r2 = self.copy()
        r2.translate(v)
        return r2

    def init_from_vectors(self,position,dimension):
        """ Initialise from vector pos and dim """
        self.position = position
        self.dimension = dimension

    def get_points(self):
        return self.get_poly().get_points()

    def get_poly(self):
        """ Returns a polygon of the Rect (cf Polygon) """
        (l,t,w,h) = self.get_coord()
        v1 = Vector(l,t)
        v2 = Vector(l+w,t)
        v3 = Vector(l+w,t+h)
        v4 = Vector(l,t+h)
        box = Polygon([v1,v2,v3,v4])
        return box

    def point_in(self,v):
        """ Returns True if v is in this rectangle """
        (l,t,w,h) = self.get_coord()
        min_x=min(l,l+w)
        max_x=max(l,l+w)
        min_y=min(t,h+t)
        max_y=max(t,h+t)
        return (min_x <= v.x <= max_x) and (min_y <= v.y <= max_y)

    def collide_poly(self,poly):
        """ Returns true if self, collides with poly """
        sfpoly = self.get_poly()
        return sfpoly.collide(poly)

    def nearest_wall(self,point):
        """ Returns the nearest wall of point (index,distance) with index = 0 for top, 1, rigth; 2,bot; 3,left"""
        (l,t,w,h) = self.get_coord()
        dtop = abs(t - point.y)
        dbot = abs(t+h-point.y)
        dleft = abs(l - point.x)
        dright = abs(l+w-point.x)
        li = [dleft,dtop,dright,dbot]
        index = np.argmin(li)
        return index,li[index]

    def get_max_x(self):
        return self.get_position().x+self.get_dimension().x

    def get_max_y(self):
        return self.get_position().y+self.get_dimension().y

    def get_min_x(self):
        return self.get_position().x

    def get_min_y(self):
        return self.get_position().y

    def get_position(self):
        return self.position

    def get_dimension(self):
        return self.dimension

    def set_position(self,pos):
        self.position = pos

    def set_dimension(self,dim):
        self.dimension = dim

    def to_tuples(self):
        """ Returns the rect as a list of tuples """
        li = []
        for p in self.get_points():
            li.append( (p.x,p.y) )
        return li

    def to_pygame(self):
        (l,t,w,h) = self.get_coord()
        return pygame.Rect(l,t,w,h)
