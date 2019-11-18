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
        
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
        self.transform = Transform()
        self.rotation = Transform()
        self.inv_transform = Transform()

    def __eq__(self,rect):
        bl = self.left == rect.left
        bt = self.top == rect.top
        bw = self.width == rect.width
        bh = self.height == rect.height
        bt = self.transform == rect.transform
        return bl and bt and bw and bh and bt

    def __str__(self):
        return "Rect("+str(self.left)+","+str(self.top)+","+str(self.left+self.width)+","+str(self.top+self.height)+")"

    def copy(self):
        """ Returns a copy of this vector """
        r2 = Rect(self.left,self.top,self.width,self.height)
        r2.transform = self.transform.copy()
        r2.rotation = self.rotation.copy()
        r2.inv_transform = self.inv_transform
        return r2

    
    def init_from_vectors(self,position,size):
        self.left = position.x
        self.top = position.y
        self.width = size.x
        self.height = size.y

    def get_points(self):
        return self.get_box().get_points()

    def get_box(self):
        box = Polygon([Vector(self.left,self.top),Vector(self.left+self.width,self.top),Vector(self.left+self.width,self.top+self.height),Vector(self.left,self.top+self.width)])
        return box.apply_transform(self.transform)

    def refresh_inverse(self):
        self.inv_transform = self.transform.get_inverse()

    def translate(self,v):
        self.transform = self.transform.translate(v)
        self.refresh_inverse()

    def translate2(self,v):
        tr = self.transform.translate(v)
        tr.refresh_inverse()
        return tr

    def rotate(self,a):
        self.transform = self.transform.rotate(a)
        self.rotation = self.rotation.rotate(a)
        self.refresh_inverse()

    def scale(self,s):
        self.transform = self.transform.scale(s)
        self.refresh_inverse()
        
    def point_in(self,v):
        min_x=min(self.left,self.left+self.width)
        max_x=max(self.left,self.left+self.width)
        min_y=min(self.top,self.height+self.top)
        max_y=max(self.top,self.height+self.top)
        return (min_x <= v.x <= max_x) and (min_y <= v.y <= max_y)

    def apply_transform(self,t):
        r = self.copy()
        r.transform = r.transform.combine(t)
        r.refresh_inverse()
        return r

    def points_in(self,rect2):
        """ Returns points from self that are in rect 2, in the referential of rect2 """
        poly = self.get_box().apply_transform(rect2.inv_transform)
        l = []
        for p in poly.get_points():
            if rect2.point_in(p):
                l.append(p)
        return l

    def collide(self,rect2):
        return self.points_in(rect2) + rect2.points_in(self)
    
    def remove_collide(self,rect2):
        epsilon = 0.0001
        pf = self.points_in(rect2)
        p2 = rect2.points_in(self)
        #print("self",self.get_box())
        #print("rect2",rect2.get_box())
        #print("pf p2",pf,p2)
        if pf + p2 == []:
            return (Vector(0,0),Vector(0,0))
        elif len(pf) == 1 and p2 == []:
            point = pf[0]
            nwi,d = rect2.nearest_wall(point)
            #print("nwi,d",nwi,d)
            v = rect2.wall_index_to_vector(nwi)*d
            #print("v",v)
            return v.apply_transform(rect2.transform.cut_translate())*(1+epsilon)
        elif pf == [] and len(p2) == 1:
            nwi,d = self.nearest_wall(p2[0])
            #print("nwi,d",nwi,d)
            v = self.wall_index_to_vector(nwi)*d
            #print("v",v)
            return -v.apply_transform(self.transform.cut_translate())*(1+epsilon)
        elif len(pf) == 1 and len(p2) == 1:
            nwi,d = self.nearest_wall(p2[0])
            #print("nwi,d",nwi,d)
            v = self.wall_index_to_vector(nwi)*d
            #print("v",v)
            return -v.apply_transform(self.transform.cut_translate())*(1+epsilon)
        else:
            print("self",self.get_box())
            print("rect2",rect2.get_box())
            print("pf",pf)
            print("p2",p2)
            assert False #Not handled by physics

    def nearest_wall(self,point):
        dtop = abs(self.top - point.y)
        dbot = abs(self.top+self.height-point.y)
        dleft = abs(self.left - point.x)
        dright = abs(self.left+self.width-point.x)
        li = [dleft,dtop,dright,dbot]
        index = np.argmin(li)
        return index,li[index]

    def wall_index_to_vector(self,index):
        if index == 0:
            return Vector(-1,0)
        elif index == 1:
            return Vector(0,-1)
        elif index == 2:
            return Vector(1,0)
        elif index == 3:
            return Vector(0,1)
        else:
            assert False #Wrong index in Rect.wall_index_to_vector

    def to_tuples(self):
        li = []
        for p in self.get_points():
            li.append( (p.x,p.y) )
        return li
            

    """
    def contains_vect(self,v):
        return self.contains(v.x,v.y)

    def intersects(self,rect):
        r1_min_x=min(self.__left,self.__left+self.__width)
        r1_max_x=max(self.__left,self.__left+self.__width)
        r1_min_y=min(self.__top,self.__top+self.__height)
        r1_max_y=max(self.__top,self.__top+self.__height)

        r2_min_x=min(rect.__left,rect.__left+rect.__width)
        r2_max_x=max(rect.__left,rect.__left+rect.__width)
        r2_min_y=min(rect.__top,rect.__top+rect.__height)
        r2_max_y=max(rect.__top,rect.__top+rect.__height)

        inter_left=max(r1_min_x,r2_min_x)
        inter_top=max(r1_min_y,r2_min_y)
        inter_right=min(r1_max_x,r2_max_x)
        inter_bot=min(r1_max_y,r2_max_y)

        if inter_left < inter_right and inter_top < inter_bot:
            return Rect(\
                    left=inter_left,\
                    top=inter_top,\
                    width=inter_right-inter_left,\
                    height=inter_bot-inter_top)
        else:
            return None
    """

    def get_position(self):
        return Vector(x=self.left,y=self.top)

    def get_dimension(self):
        return Vector(x=self.width,y=self.height)

    def set_position(self,pos):
        (self.left,self.top) = (pos.x,pos.y)

    def set_dimension(self,dim):
        (self.width,self.height) = (dim.x,dim.y)

    def to_pygame(self):
        return pygame.Rect(self.left,self.top,self.width,self.height)
