from controlableNode import ControlableNode
from spriteScheduler import *
from hitbox import Hitbox
from rect import Rect
from player import Player
from items import KeyItem

""" Key class to show interactions between game and campaign"""

class Coin(ControlableNode):
    def __init__(self,hb,name='empty'):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_collide(True)
        self.create_sps("coin")
        self.center_hit_box()

        self.taken = False
        self.key = KeyItem("no_key") #A changer

    def center_hit_box(self):
        self.get_hit_box().center()

    def copy(self):
        """ Returns the copy of this """
        sd = SolidPlatform(Hitbox(Rect(0,0,0,0)))
        self.paste_in(sd)
        return sd

    def paste_in(self,t):
        ControlableNode.paste_in(self,t)

    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                o2.add_score(100)
                self.taken = True
                #Remove the coin
                self.create_sps('empty')
                self.set_state('s')
                
    
