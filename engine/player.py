import sys
import os
import numpy as np
import pygame
from collections import defaultdict

path = os.getcwd()
path += "/engine"
sys.path.append(path)

from jumpableNode import JumpableNode
from solidPlatform import SolidPlatform
from controller import KeyboardController
from hitbox import Hitbox
from rect import Rect
from vector import Vector
from projectile import Projectile
import mob

""" The player object -> represents the player controllableNode """

class Player(JumpableNode):
    """ Player Class """
    def __init__(self):
        super().__init__()
        self.set_hit_box(Hitbox(Rect(-1,-2,12,16))) #Specific Hit box
        self.set_rigid_body(True) #it's a rigid body

        self.create_sps("player") #Set sprite
        self.animation_speed = 0.05
        self.set_state("r") #First state : runing ('r')
        self.controller = PlayerController(self) #Controller for the player (see below)
        self.score = 0 #Score of the player

        self.small = False #Life bar

        self.is_in_air = True #Is acutally in the air

        self.inventory = defaultdict(int) #Ref to inventory to give items to Campaign mod

        self.score_to_add = 0 #Score to add for animations

    def __repr__(self):
        return "Player("+str(self.get_hit_box())+")"

    def copy(self):
        raise NotImplemented

    def paste_in(self,p):
        raise NotImplemented

    def end_init(self):
        self.add_force(self.world.gravity)

    def load_inventory(self,inv):
        """ Load the inventory of campaign mod """
        self.inventory = inv

    def set_inventory(self,items):#Should be renamed to add_inventory
        """ Add in inventory the aforementiened items"""
        for item in items:
            if item.type != "key":#item.type == "csm": #For consommable (may have several)
                self.inventory[item] += items[item]
            else:
                self.inventory[item] = items[item]

    def get_inventory(self):
        return self.inventory


    def collide(self,o,side,o2_side):
        """ Player collides with o """
        #print("collide",self,o,side,o2_side)
        if isinstance(o,SolidPlatform):
            if o2_side == 0 or o2_side == 1:
                #Top side
                if self.alive:
                    self.set_state("r") #For the spriteScheduler -> state run (r)
                self.allow_jump()
                self.is_jumping = False
                self.is_in_air = False
            else:
                if self.is_in_air:
                    #The player dies
                    self.die()
        if isinstance(o,mob.Mob):
            self.take_damages(o.damages)

        if isinstance(o,Projectile) and o.lifecollide:
            self.take_damages(o.damages)

    def die(self):
        """ Kills the player """
        self.set_state("d") #For the spriteScheduler -> state die (d)
        super().die()

    def update(self):
        """ Update var """
        self.can_jump = False #Pour qu'on ne puisse pas sauter dans les airs
        self.is_in_air = True #Pour la detection de la mort : le joueur doit être en l'air et entrer en collision

        if self.alive:
            self.set_state("j") #For the spriteScheduler -> state jump (j)

        if self.score_to_add > 0:
            valadd = min(50,self.score_to_add)
            valprod = int(self.score_to_add/10+0.5)
            val = max(valadd,valprod)
            self.score += val
            self.score_to_add -= val

    def flush_score(self):
        self.score += self.score_to_add
        self.score_to_add = 0

    def add_score(self,val):
        self.score_to_add += val

    def get_score(self):
        return self.score

class PlayerController(KeyboardController):
    """ Controller for the player """
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        """ Execute controller code """
        jump_key = pygame.K_z
        if (event is not None and event.type == pygame.KEYDOWN and event.key == jump_key) or pressed[jump_key]:
            self.target.start_jump()
        if event is not None and event.type == pygame.KEYUP:
            if event.key == jump_key:
                self.target.stop_jump()
        self.target.update()
