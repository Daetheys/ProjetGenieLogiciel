from controlableNode import ControlableNode
from spriteScheduler import *
from hitbox import Hitbox
from rect import Rect
import copy

""" A standard platform of the game """

class SolidPlatform(ControlableNode):
    """ SolidPlatform of the game """
    def __init__(self,hb,name='empty'):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_rigid_body(True)
        self.set_sps(SpriteScheduler("platform"))
        self.get_sps().load_automaton()
        self.get_sps().load_sprites()
        self.center_hit_box()
        self.mapping = "Repeatx"

    def center_hit_box(self):
        """ Centers the hitbox """
        self.get_hit_box().center()

    def copy(self):
        """ Returns the copy of this """
        sd = SolidPlatform(Hitbox(Rect(0,0,0,0)))
        self.paste_in(sd)
        return sd

    def paste_in(self,t):
        ControlableNode.paste_in(self,t)

    def __repr__(self):
        return "SolidPlatform("+str(self.get_position())+","+str(self.get_hit_box())+")" 

    def collide(self,o2,side,o2_side):
        """ Function called when this collides something else -> nothing to do there"""
        pass



'''
not used anymore
from vector import Vector
class Pattern(SolidPlatform):
    """ class Pattern.
    Solidplatforms in level that are moving along some pattern
    can now be considered as patterns objects. Be sure to type the right
    patternYype in the self.pt field.  """

    def __init__(self,polygon,name='empty'):
        SolidPlatform.__init__(self,polygon,name)
        self.pt = ""#patternType
        self.period = 1
        self.init_delay = 0
        self.speed = 1

    def pattern(self,t):
        """
        PatternType |What this function does
            ""      | it does not move the sprite
         "UpDown"   | the sprite moves down or up
        """
        if self.pt == "UpDown":
            if t > self.init_delay:
                if (t-self.init_delay) % self.period < self.period/2:
                    self.translate(Vector(0,self.speed))
                else:
                    self.translate(Vector(0,-self.speed))
        elif self.pt == "Square":
            if t > self.init_delay:
                if (t-self.init_delay) % self.period < self.period/4:
                    self.translate(Vector(0,self.speed))
                elif (t-self.init_delay) % self.period < self.period/2:
                    self.translate(Vector(self.speed,0))
                elif (t-self.init_delay) % self.period < 3*self.period/4:
                    self.translate(Vector(0,-self.speed))
                else:
                    self.translate(Vector(-self.speed,0))

'''
