#!/usr/bin/env python3


class Map_Point:    #abstract class

    def __init__(self,x,y,img,imgf):
        self._accessible = False
        self._accessed = False
        self._finished = False
        self._start_dialogue = None
        self._end_dialogue = None
        self.x = x
        self.y = y
        self.__image = img
        self.__image_finished = imgf

    def set_start_dialogue(self, dialogue):
        self._start_dialogue = dialogue

    def set_end_dialogue(self, dialogue):
        self._end_dialogue = dialogue

    def get_start_dialogue(self):
        return self._start_dialogue

    def get_end_dialogue(self):
        return self._end_dialogue

    def get_image(self):
        if self._finished:
            return self.__image_finished
        else:
            return self.__image
