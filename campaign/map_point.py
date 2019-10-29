#!/usr/bin/env python3

#from dialogue import Dialogue


class Map_Point:
    
    def __init__(self):
        self.__accessible = False
        self.__accessed = False
        self.__finished = False
        self.__start_dialogue = None
        self.__end_dialogue = None
        
    def set_start_dialogue(self, dialogue):
        self.__start_dialogue = dialogue
        
    def set_end_dialogue(self, dialogue):
        self.__end_dialogue = dialogue
        
    def get_start_dialogue(self):
        return self.__start_dialogue
        
    def get_end_dialogue(self):
        return self.__end_dialogue