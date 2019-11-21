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

class Player(ControlableNode):
    def __init__(self):
        ControlableNode.__init__(self)
        self.set_hit_box(Hitbox(Rect(-1,-2,2,4)))
        self.set_rigid_body(True)
        self.set_sps(None)
        #self.get_sps().load_automaton()
        #self.get_sps().load_sprites()
        self.controller = PlayerController(self)
        self.score = 0
        
        self.jump_strength = 0.3
        self.can_jump = False
        self.jump_size_max = 15
        self.jump_size = self.jump_size_max

    def refresh_jump(self):
        if self.can_jump and self.jump_size > 0:
            self.set_speed(self.get_speed()+Vector(0,-self.jump_strength))
            self.jump_size -= 1

    def stop_jump(self):
        self.can_jump = False
        self.jump_size = self.jump_size_max

    def allow_jump(self):
        self.can_jump = True

    def collide(self,o):
        if isinstance(o,SolidPlatform):
            self.allow_jump()

    def get_score(self):
        return self.score

class PlayerController(KeyboardController):
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed):
        if event is not None and event.type == pygame.KEYUP:
            print("up")
            if event.key == pygame.K_z:
                self.target.stop_jump()
        print("-",pressed[pygame.K_z])
        if pressed[pygame.K_z]:
            print("refresh")
            self.target.refresh_jump()
