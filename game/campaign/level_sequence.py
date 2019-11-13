#!/usr/bin/env python3

from map_point import Map_Point

class Level_Sequence(Map_Point):
    
    def __init__(self,x,y,img,imgf,g):
        Map_Point.__init__(self,x,y,img,imgf,g)
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
        self.__accessible = True
        
    def is_accessed(self):
        self.__accessed = True
        
    def is_finished(self):
        self.__finished = True
        for child in self.__childs:
            child.is_accessible
        
    def launch(self,g):
        if self._start_dialogue is not None:
            self._start_dialogue.show(g)
        self.is_accessed()
        for level in self.__levels:
            level.launch()
        self.is_finished()
        if self._end_dialogue is not None:
            self._end_dialogue.show(g)
        return True,False