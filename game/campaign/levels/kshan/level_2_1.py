
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
            return t*2000 #*8 to be faster (but it doesn't match the music anymore !
            
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            
        objects = self.init_objects(g)

        gl = GameLevel(objects,player_pos,name="level_2_1_kshan")
        
        #g.launch_music(text)
        
        success = self.check_victory(g, g.launch_level(gl))
        pygame.event.get()#to capture inputs made during the wait
        
        
        if success:
            self.fun_dialogue(g,"good_end")
            self.set_finished()
            self.reward(g)
        else:
            self.fun_dialogue(g,"bad_end")
        
        return success
    
    def init_objects(self,g):
        plat_1 = SolidPlatform(Hitbox(Rect(-10,12,100,24)))
        plat_1.set_sps(None)#voir une hitbox
        
        plat_2 = SolidPlatform(Hitbox(Rect(120,16,300,28)))
        plat_2.set_sps(None)#voir une hitbox
        
        plat_3 = SolidPlatform(Hitbox(Rect(310,2,450,14)))
        plat_3.set_sps(None)#voir une hitbox
        
        plat_4 = SolidPlatform(Hitbox(Rect(500,4,680,16)))
        plat_4.set_sps(None)#voir une hitbox
        
        plat_5 = SolidPlatform(Hitbox(Rect(700,14,780,26)))
        plat_5.set_sps(None)#voir une hitbox
        
        plat_6 = SolidPlatform(Hitbox(Rect(790,14,860,26)))
        plat_6.set_sps(None)#voir une hitbox
        
        plat_7 = SolidPlatform(Hitbox(Rect(890,12,980,24)))
        plat_7.set_sps(None)#voir une hitbox
        
        plat_8 = SolidPlatform(Hitbox(Rect(1010,20,1120,32)))
        plat_8.set_sps(None)#voir une hitbox
        
        plat_9 = SolidPlatform(Hitbox(Rect(1140,18,1400,30)))
        plat_9.set_sps(None)#voir une hitbox
        
        return [plat_1,plat_2,plat_3,plat_4,plat_5,plat_6,plat_7,plat_8,plat_9]