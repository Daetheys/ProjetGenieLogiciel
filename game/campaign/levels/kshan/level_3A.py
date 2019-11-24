
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
from key import Key_1
from gameLevel import GameLevel
from hypothesis import given
from hypothesis.strategies import integers, lists
from hitbox import Hitbox
from rect import Rect
from level import Level
from items import KeyItem

class Level_3A_kshan(Level):
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan3Adv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan3A"].show(g)
        elif arg == "bad_end_1":
            quit_all = g.dict_dial["dial_kshan3Abf1"].show(g)
        elif arg == "bad_end_2":
            quit_all = g.dict_dial["dial_kshan3Abf2"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan3Agf"].show(g)
        return quit_all
        
    def check_victory(self,g,arg):
        if arg and g.player.is_in_inventory(self.key.key):
            return True
        return False
        
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100 #*8 to be faster (but it doesn't match the music anymore !
            
        #objects = self.init_objects(g)

        gl = GameLevel(self.objects,player_pos,name="level_3A_kshan")
        gl.load_inventory(g.player.get_inventory())
        
        #g.launch_music(text)
        
        alive = g.launch_level(gl,None)
        success = self.check_victory(g, alive)
        pygame.event.get()#to capture inputs made during the wait
        
        
        if success:
            self.fun_dialogue(g,"good_end")
            self.set_finished()
            self.reward(g)
        else:
            if alive:
                self.fun_dialogue(g,"bad_end_2")
            else:
                self.fun_dialogue(g,"bad_end_1")
        
        return success
    
    def init_objects(self,g):
        plat = []
        dist = -10
        for i in range(10):
            l = (i+1)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,-10,l,18))))
            dist += l + 20
        plat.append(SolidPlatform(Hitbox(Rect(dist,-26,500,24))))
        self.key = Key_1(Hitbox(Rect(dist+300,-58,4,4)))
        plat.append(self.key)
        dist += 520
        for i in range(17):
            l = (i+5)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,-10,l,18))))
            dist += l + 20
        
        return plat