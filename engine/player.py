import sys
import os
import numpy as np
import pygame

path = os.getcwd()
path += "/engine"
sys.path.append(path)

from controlableNode import ControlableNode
from solidPlatform import SolidPlatform
from controller import KeyboardController
from hitbox import Hitbox
from rect import Rect
from vector import Vector
from force import Jump

class Player(ControlableNode):
    """ Player Class """
    def __init__(self):
        ControlableNode.__init__(self)
        self.set_hit_box(Hitbox(Rect(-1,-2,2,4)))
        self.set_rigid_body(True)
        self.set_sps(None)
        #self.get_sps().load_automaton()
        #self.get_sps().load_sprites()
        self.controller = PlayerController(self)
        self.score = 0
        
        self.jump_strength = 0.5
        self.can_jump = False
        self.jump_size_max = 7
        self.jump_size = self.jump_size_max

    def refresh_jump(self):
        """ Key actually pressed """
        if self.can_jump and self.jump_size > 0:
            self.set_speed(self.get_speed()+Vector(0,-self.jump_strength))
            self.jump_size -= 1

    def start_jump(self):
        """ Key has just been pressed """
        pass

    def stop_jump(self):
        """ Key has just been released """
        self.can_jump = False
        self.jump_size = self.jump_size_max

    def allow_jump(self):
        """ Allow the player to jump """
        self.can_jump = True

    def collide(self,o):
        """ Player collides with o """
        if isinstance(o,SolidPlatform):
            self.allow_jump()

    def add_score(self,val):
        self.score += val

    def get_score(self):
        return self.score

class PlayerController(KeyboardController):
    """ Controller for the player """
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed):
        """ Execute controller code """
        if event is not None and event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                self.target.stop_jump()
        """if event is not None and event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                self.target.start_jump()"""
        if pressed[pygame.K_z]:
            self.target.refresh_jump()
