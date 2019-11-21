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
        self.jump_strength = 5
        self.can_jump = False

    def jump(self):
        if self.can_jump:
            self.set_speed(self.get_speed()+Vector(0,-self.jump_strength))
            self.can_jump = False

    def allow_jump(self):
        self.can_jump = True

    def collide(self,o):
        #print("Player collide")
        if isinstance(o,SolidPlatform):
            self.allow_jump()

    def get_score(self):
        return self.score

class PlayerController(KeyboardController):
    def __init__(self,target=None):
        super().__init__()

    def execute(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                print("JUMP")
                self.target.jump()
