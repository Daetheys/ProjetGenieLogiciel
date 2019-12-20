from lifeableNode import LifeableNode
from controller import KeyboardController
from vector import Vector
from projectile import Projectile

import solidPlatform
from hitbox import Hitbox
from rect import Rect

class JumpableNode(LifeableNode):
    """ Jumpable Class """
    def __init__(self):
        super().__init__()

        self.jump_strength = 500 #Strength of the jump
        self.can_jump = True #Can jump
        self.is_jumping = False #Is actually jumping

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

class JumpableController(KeyboardController):
    """ Controller for the jumpable """
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