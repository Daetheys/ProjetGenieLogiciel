#!/usr/bin/env python3

from map import Map


class World:
    
    def __init__(self):
        self.__maps = {}
        
    def set_maps(self, maps):
        for map in maps:
            self.__maps[map.name] = map
        
    def get_map(self,name):
        return self.__maps[name]