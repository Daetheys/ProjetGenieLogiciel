#!/usr/bin/env python3

class Map:
    '''A map is an object smaller than a world, it has an image and contains map_points (who are abstract classes containing level sequences)'''

    def __init__(self,img_surf,name,music="data/musics/title.ogg"):
        self.__map_points = []
        self.__accessible = False
        self.__accessed = False
        self.__finished = False
        self.name = name
        self.image = img_surf
        self.music = music

    def set_map_points(self, map_points):
        self.__map_points = map_points

    def get_map_points(self):
        return self.__map_points

    def activation(self):
        self.__accessible = True

    def is_accessed(self):
        self.__accessed = True

    def is_finished(self):
        self.__finished = True
