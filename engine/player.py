import sys
import os
import numpy as np
import pygame
from collections import defaultdict

path = os.getcwd()
path += "/engine"
sys.path.append(path)

from controlableNode import ControlableNode
from solidPlatform import SolidPlatform
from controller import KeyboardController
from hitbox import Hitbox
from rect import Rect
from vector import Vector

""" The player object -> represents the player controllableNode """

class Player(ControlableNode):
    """ Player Class """
    def __init__(self):
        ControlableNode.__init__(self)
        self.set_hit_box(Hitbox(Rect(-1,-2,12,16))) #Specific Hit box
        self.set_rigid_body(True) #it's a rigid body

        self.create_sps("player") #Set sprite
        self.set_state("r") #First state : runing ('r')
        self.controller = PlayerController(self) #Controller for the player (see below)
        self.score = 0 #Score of the player
        self.alive = True #He is alive ... for now

        self.jump_strength = 500 #Strength of the jump
        self.can_jump = True #Can jump
        self.is_jumping = False #Is actually jumping

        self.is_in_air = True #Is acutally in the air

        self.inventory = defaultdict(int) #Ref to inventory to give items to Campaign mod

    def load_inventory(self,inv):
        """ Load the inventory of campaign mod """
        self.inventory = inv

    def set_inventory(self,items):
        """ Add in inventory """
        for item in items:
            if item.type == "csm": #For consommable (may have several)
                self.inventory[item] += items[item]
            else:
                self.inventory[item] = items[item]

    def get_inventory(self):
        return self.inventory

    def start_jump(self):
        """ Key has just been pressed """
        speed = self.get_speed()
        if self.can_jump and (not self.is_jumping) and speed.y >= 0:
            self.set_speed(Vector(speed.x, -self.jump_strength)) #JUMP
            self.can_jump = False #Cannot jump anymore

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
            if o2_side == 0 or o2_side == 1:
                #Top side

                if self.can_jump and self.alive:
                    self.set_state("r") #For the spriteScheduler -> state run (r)
                self.allow_jump()
                self.is_jumping = False
                self.is_in_air = False



            else:
                if self.is_in_air:
                    #The player dies
                    self.die()

    def die(self):
        """ Kills the player """
        self.set_state("d") #For the spriteScheduler -> state die (d)
        print("Player Dies")
        self.alive = False

    def update(self):
        """ Update var """
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
