#!/usr/bin/env python3

from map import Map


class World:
    
    def __init__(self):
        self.__maps = []
        
    def set_maps(self, maps):
        self.__maps = maps
        
    def get_maps(self):
        return self.__maps