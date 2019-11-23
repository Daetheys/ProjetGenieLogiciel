#!/usr/bin/env python3


class Map_Point:    #abstract class

    def __init__(self,name,x,y,img,imgf):
        self._accessible = False
        self._accessed = False #maybe useless
        self._finished = False
        self.x = x
        self.y = y
        self.name = name
        self.__image = img
        self.__image_finished = imgf


    def get_image(self):
        if self._finished:
            return self.__image_finished
        else:
            return self.__image
