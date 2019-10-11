#!/usr/bin/env python3

class Rect:
    def __init__(self):
        self.__left = 0.
        self.__top = 0.
        self.__width = 0.
        self.__height = 0.

    def __init__(self,left,top,width,height):
        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height

    def init(self,position,size):
        self.__left = position.x
        self.__top = position.y
        self.__width = size.x
        self.__height = size.y

    def contains(self,x,y):
        min_x=min(self.__left,self.__left+self.__width)
        max_x=max(self.__left,self.__left+self.__width)
        min_y=min(self.__top,self.__right+self.__top)
        max_y=max(self.__top,self.__right+self.__top)
        return (min_x <= x <= max_x) && (min_y <= y <= max_y)

    def contains(self,v):
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
        inter_right=max(r1_max_x,r2_max_x)
        inter_bot=max(r1_max_y,r2_max_y)

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

    def get_size(self):
        return Vector(x=self.__width,y=self.__height)
