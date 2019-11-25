#!/usr/bin/env python3

'''A world is the biggest object of the campaign that contains all the map'''


class World:
    
    def __init__(self):
        self.__maps = {}
        
    def set_maps(self, maps):
        """set the maps of the world"""
        for map in maps:
            self.__maps[map.name] = map
        
    def get_map(self,name):
        """return the map with the name"""
        return self.__maps[name]
        
    def get_maps(self):
        """return all the maps"""
        return self.__maps