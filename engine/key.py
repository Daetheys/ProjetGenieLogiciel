from pickableNode import PickableNode
from spriteScheduler import *
from hitbox import Hitbox
from rect import Rect
from player import Player
from items import KeyItem

""" Key class to show interactions between game and campaign"""

class Key_1(PickableNode):
    def __init__(self,hb,name='empty'):
        PickableNode.__init__(self,hb,name='empty')
        self.create_sps("key")
        self.key = KeyItem("key_1")

    def center_hit_box(self):
        self.get_hit_box().center()

    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                o2.set_inventory({self.key:1})
                self.taken = True
                self.create_sps('empty')
                self.set_state('s')
                
    
