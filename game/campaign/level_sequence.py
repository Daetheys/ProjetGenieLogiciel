#!/usr/bin/env python3

from map_point import Map_Point
import pygame   #for ugly code

class Level_Sequence(Map_Point):

    def __init__(self,name,x,y,img,imgf):
        Map_Point.__init__(self,name,x,y,img,imgf)
        self.__levels = []
        self.__childs = []

    def set_levels(self, levels):
        self.__levels = levels

    def get_levels(self):
        return self.__levels

    def set_childs(self, childs):
        self.__childs = childs

    def get_childs(self):
        return self.__childs

    def set_accessible(self):
        self._accessible = True

    def set_accessed(self): #maybe useless
        self._accessed = True

    def set_finished(self):
        self._finished = True
        for child in self.__childs:
            child.set_accessible()

    def get_accessible(self):
        return self._accessible

    def get_accessed(self):
        return self._accessed

    def get_finished(self):
        return self._finished

    def launch(self,g):
        self.set_accessed() #is it useful ?
        reussite = True #pour réussir, il faut gagner tous les levels du level_sequence
        for level in self.__levels:
            reussite = reussite and level.launch(g)
        if reussite:
            self.set_finished()

        g.launch_music(g.menu_music)#relance la musique du menu

        return True,False
