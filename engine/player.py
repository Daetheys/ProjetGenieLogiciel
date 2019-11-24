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
        self.set_hit_box(Hitbox(Rect(-1,-2,12,16)))
        self.set_rigid_body(True)

        self.create_sps("player")
        self.set_state("r")
        #self.set_sps(None)
        #self.get_sps().load_automaton()
        #self.get_sps().load_sprites()
        self.controller = PlayerController(self)
        self.score = 0
        self.alive = True
        
        self.jump_strength = 500
        self.can_jump = True
        self.is_jumping = False

        self.is_in_air = False

        self.jump_invincibility_max = 2
        self.jump_invincibility_countdown = 0

    def start_jump(self):
        """ Key has just been pressed """
        speed = self.get_speed()
        #print(self.can_jump, not self.is_jumping, speed.y >= 0)
        if self.can_jump and (not self.is_jumping) and speed.y >= 0:
            self.set_speed(Vector(speed.x, -self.jump_strength))
            self.can_jump = False

    def stop_jump(self):
        """ Key has just been released """
        speed = self.get_speed()
        self.set_speed(Vector(speed.x,0))
        self.is_jumping = False

    def allow_jump(self):
        """ Allow the player to jump """
        self.can_jump = True

    def collide(self,o,side,o2_side):
        """ Player collides with o """
        if isinstance(o,SolidPlatform):
            if o2_side == 0:
                #Top side

                if self.can_jump and self.alive:
                    self.set_state("r") #For the spriteScheduler -> state run (r)
                self.allow_jump()
                self.is_jumping = False
                self.is_in_air = False
                self.jump_invincibility_countdown = self.jump_invincibility_max

                
            else:
                if self.is_in_air and self.jump_invincibility_countdown>0:
                    #The player dies
                    self.die()
                self.jump_invincibility_countdown -= 1

    def die(self):
        """ Kills the player """
        self.set_state("d") #For the spriteScheduler -> state die (d)
        print("Player Dies")
        self.alive = False

    def update(self):
        self.can_jump = False #Pour qu'on ne puisse pas sauter dans les airs
        self.is_in_air = True #Pour la detection de la mort : le joueur doit être en l'air et entrer en collision
        #
        if self.alive:
            self.set_state("j") #For the spriteScheduler -> state jump (j)
            
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
        jump_key = pygame.K_z
        if (event is not None and event.type == pygame.KEYDOWN and event.key == jump_key) or pressed[jump_key]:
            self.target.start_jump()
        if event is not None and event.type == pygame.KEYUP:
            if event.key == jump_key:
                self.target.stop_jump()
        self.target.update()
