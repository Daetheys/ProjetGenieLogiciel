from engine.controlableNode import ControlableNode
from engine.spriteScheduler import *
from engine.hitbox import Hitbox
from engine.rect import Rect
import copy

""" A standard platform of the game """

class SolidPlatform(ControlableNode):
    """ SolidPlatform of the game """
    def __init__(self,hb,name='empty',sps='platform'):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_rigid_body(True)
        self.set_sps(SpriteScheduler(sps))
        self.get_sps().load_automaton()
        self.get_sps().load_sprites()
        self.center_hit_box()
        self.mapping = "Repeatx"
        if sps == "platform":
            self.y_offset -= 20

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
