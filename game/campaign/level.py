#!/usr/bin/env python3

import pygame

class Level:
    
    def __init__(self):
        self.__useless = True
        
    def launch(self):
        #launch the level
        pygame.time.wait(2000)  #useless...
        return True #for now, if we launch a level, we win