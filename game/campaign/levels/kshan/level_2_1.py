
import sys
import os
#import numpy as np
import pygame
from pygame.locals import *
path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform,Pattern
from gameLevel import GameLevel
from hypothesis import given
from hypothesis.strategies import integers, lists
from hitbox import Hitbox
from rect import Rect
from level import Level

class Level_2_1_kshan(Level):
    
    def __init__(self):
        super().__init__()
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            g.dict_dial["dial_kshan2"].show(g)
        elif arg == "bad_end":
            g.dict_dial["dial_kshan2f"].show(g)
        elif arg == "good_end":
            g.dict_dial["dial_kshan2f"].show(g)
        
    def check_victory(self,g,arg):
        return arg
        
    def launch(self,g):
        self.set_accessed()
        self.fun_dialogue(g,"start")
        
        def player_pos(t):
            return t*100 #*8 to be faster (but it doesn't match the music anymore !
            
            
        objects = self.init_objects(g)

        gl = GameLevel(objects,player_pos,name="level_2_1_kshan")
        
        #g.launch_music(text)
        
        success = self.check_victory(g, g.launch_level(gl,None))
        pygame.event.get()#to capture inputs made during the wait
        
        
        if success:
            self.fun_dialogue(g,"good_end")
            self.set_finished()
            self.reward(g)
        else:
            self.fun_dialogue(g,"bad_end")
        
        return success
    
    def init_objects(self,g):
        plat = []
        for i in range(10):
            plat.append(SolidPlatform(Hitbox(Rect((i*120)-10,-10,100,18))))
        
        return plat