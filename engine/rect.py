#!/usr/bin/env python3
import os
import sys
from vector import Vector
path = os.getcwd()
path += "/error"
sys.path.append(path)
from exception import WrongRectWidth,WrongRectHeight

class Rect:
    """ The Y axis is directed to bottom """
    def __init__(self,left=0,top=0,width=0,height=0):
        if width<0:
            raise WrongRectWidth()
        if height<0:
            raise WrongRectHeight()
        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height

    def __eq__(self,rect):
        bl = self.__left == rect.__left
        bt = self.__top == rect.__top
        bw = self.__width == rect.__width
        bh = self.__height == rect.__height
        return bl and bt and bw and bh

    def __str__(self):
        return "left:"+str(self.__left)+" top:"+str(self.__top)+" width:"+str(self.__width)+" height:"+str(self.__height)

    def init(self,position,size):
        self.__left = position.x
        self.__top = position.y
        self.__width = size.x
        self.__height = size.y

    def contains(self,x,y):
        min_x=min(self.__left,self.__left+self.__width)
        max_x=max(self.__left,self.__left+self.__width)
        min_y=min(self.__top,self.__height+self.__top)
        max_y=max(self.__top,self.__height+self.__top)
        return (min_x <= x <= max_x) and (min_y <= y <= max_y)

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

    def get_position(self):
        return Vector(x=self.__left,y=self.__top)

    def get_dimension(self):
        return Vector(x=self.__width,y=self.__height)

    def set_position(self,pos):
        (self.__left,self.__top) = (pos.x,pos.y)

    def set_dimension(self,dim):
        (self.__width,self.__height) = (dim.x,dim.y)
