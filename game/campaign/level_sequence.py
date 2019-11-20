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

    def is_accessible(self):
        self._accessible = True

    def is_accessed(self):
        self._accessed = True

    def is_finished(self):
        self._finished = True
        for child in self.__childs:
            child.is_accessible

    def launch(self,g):
        if self._start_dialogue is not None:
            quit_all = self._start_dialogue.show(g)
            if quit_all:
                return True,False#ne charge pas le level
        self.is_accessed()
        g.win().blit(g.dict_img["img_dial"],(0,400))  #ugly code just to separate start and end dialogue
        g.flip()

        reussite = []
        for level in self.__levels:
            reussite.append(level.launch(g))#pour savoir quels niveaux ont été réussis !
        self.is_finished()
        if self._end_dialogue is not None:
            self._end_dialogue.show(g)
            #la valeur de retour n'est pas utile ici, puisqu'on quitte de toute façon après.
        return True,False