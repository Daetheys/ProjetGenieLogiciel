#!/usr/bin/env python3

from map_point import Map_Point


class Map():
    
    def __init__(self):
        self.__levels = []
        self.__accessible = False
        self.__accessed = False
        self.__finished = False
        
    def set_levels(self, levels):
        self.__levels = levels
        
    def get_levels(self):
        return self.__levels