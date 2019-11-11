#!/usr/bin/env python3



class Level:
    
    def __init__(self):
        self.__childs = []
        
    def set_childs(self, childs):
        self.__childs = childs
        
    def get_childs(self):
        return self.__childs