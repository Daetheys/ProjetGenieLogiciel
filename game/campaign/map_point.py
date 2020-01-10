#!/usr/bin/env python3



class Map_Point:    #abstract class
    '''A Map_point is an abstract class for a sequence of level'''

    def __init__(self,name,x,y,img,imgf):
        self._accessible = False
        self._accessed = False #used in the dialogues : there is no more surprise in the level 2 once you have already seen it.
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
