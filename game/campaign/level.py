#!/usr/bin/env python3

import pygame
from level_1 import *
from level_2 import *

class Level:    #will be an abstract class

    def __init__(self):
        self.__useless = False

    def launch(self,g):
        """launch the level in the context of the game g"""
        #pygame.time.wait(2000)
        success = level_2_kshan(g)
        pygame.event.get()#to capture inputs made during the wait
        return success #for now, if we launch a level, we win


class Boss_Level(Level):

    def __init__(self):
        self.__useless = True

class Random_Level(Level):

    def __init__(self):
        self.__useless = True