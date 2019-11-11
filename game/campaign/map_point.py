#!/usr/bin/env python3

#from dialogue import Dialogue
import pygame

class Map_Point:

    def __init__(self,x,y,img,imgf):
        self.__accessible = False
        self.__accessed = False
        self.__finished = False
        self.__start_dialogue = None
        self.__end_dialogue = None
        self.x = x
        self.y = y
        self.__image = img
        self.__image_finished = imgf

    def set_start_dialogue(self, dialogue):
        self.__start_dialogue = dialogue

    def set_end_dialogue(self, dialogue):
        self.__end_dialogue = dialogue

    def get_start_dialogue(self):
        return self.__start_dialogue

    def get_end_dialogue(self):
        return self.__end_dialogue

    def get_image(self):
        if self.__accessible:
            return self.__image
        else:
            return self.__image_finished
