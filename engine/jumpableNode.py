from engine.lifeableNode import LifeableNode
from engine.controller import Controller
from engine.vector import Vector
from engine.projectile import Projectile
from engine.solidPlatform import SolidPlatform

from engine.hitbox import Hitbox
from engine.rect import Rect

""" Class of nodes that can jump (mobs and player will inherit of it for example) """

class JumpableNode(LifeableNode):
    """ Jumpable Class """
    def __init__(self):
        super().__init__()

        self.jump_strength = 500 #Strength of the jump
        self.can_jump = True #Can jump
        self.is_jumping = False #Is actually jumping
        self.is_in_air = True #Is acutally in the air

    def start_jump(self):
        """ Starts jump (can be called several time to jump higher """
        speed = self.get_speed()
        if self.alive and self.can_jump and (not self.is_jumping) and speed.y >= 0:
            self.set_speed(Vector(speed.x, -self.jump_strength)) #JUMP
            self.can_jump = False #Cannot jump anymore

    def stop_jump(self):
        """ Stop the jump """
        speed = self.get_speed()
        self.set_speed(Vector(speed.x,0))
        self.is_jumping = False

    def collide(self,o,side,o2_side):
        """ Handle jumping booleans to know when it's possible to jump  and when to die when hitting a platform"""
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

    def allow_jump(self):
        """ Allow the player to jump """
        self.can_jump = True

    def update(self,dt):
        """ Update jumping variables """
        super().update(dt)
        self.can_jump = False #Pour qu'on ne puisse pas sauter dans les airs
        self.is_in_air = True #Pour la detection de la mort : le joueur doit être en l'air et entrer en collision
        if self.alive:
            self.set_state("j") #For the spriteScheduler -> state jump (j)

class JumpableController(Controller):
    """ Controller for the jumpable """
    def __init__(self,target=None):
        super().__init__()
        self.target = target
