#!/usr/bin/env python3

import pygame

class Level:    #will be an abstract class
    
    def __init__(self):
        self.__useless = True
        
    def launch(self):
        #launch the level
        pygame.time.wait(2000)
        return True #for now, if we launch a level, we win


class Boss_Level(Level):
    
    def __init__(self):
        self.__useless = True