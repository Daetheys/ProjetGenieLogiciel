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
        def player_pos(t):
            return t*100 #*8 to be faster (but it doesn't match the music anymore !

        gl = GameLevel([SolidPlatform(Hitbox(Rect(10,12,20,24)))],player_pos,name="test_lvl_campaign")
        #g.launch_music(text)
        success = g.launch_level(gl)
        pygame.event.get()#to capture inputs made during the wait
        return success


class Boss_Level(Level):

    def __init__(self):
        self.__useless = True

class Random_Level(Level):

    def __init__(self):
        self.__useless = True