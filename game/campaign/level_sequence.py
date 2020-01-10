#!/usr/bin/env python3

from game.campaign.map_point import Map_Point

class Level_Sequence(Map_Point):
    '''A level sequence is a set of level that you need to pass in one go. In inherits from the abstract class Map_Point'''

    def __init__(self,name,x,y,img,imgf,map):
        Map_Point.__init__(self,name,x,y,img,imgf)
        self.__levels = []
        self.__childs = []
        self.map = map

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

    def set_accessed(self,g=None):
        """ this is used to change the dialogues
         if you have already tried the level """
        if  g is not None:
            if self.name not in g.save["accessed"]:
                g.save["accessed"].append(self.name)
        self._accessed = True

    def set_finished(self,g=None):
        self._finished = True
        if g is not None:
            if self.name not in g.save["finished"]:
                g.save["finished"].append(self.name)
        for child in self.__childs:
            child.set_accessible()
            if g is not None:
                if self.name not in g.save["accessible"]:
                    g.save["accessible"].append(child.name)

    def get_accessible(self):
        return self._accessible

    def get_accessed(self):
        return self._accessed

    def get_finished(self):
        return self._finished

    def launch(self,g):
        """ launches all levels in succession """
        self.set_accessed(g) #to change the begin dialogue
        reussite = True #pour réussir, il faut gagner tous les levels du level_sequence
        for level in self.__levels:
            reussite = reussite and level.launch(g)
        if reussite:
            self.set_finished(g)

        g.launch_music(self.map.music)#relance la musique du menu
        g.saving()
        return True,False
