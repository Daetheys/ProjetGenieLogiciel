from pickableNode import PickableNode
from spriteScheduler import *
from hitbox import Hitbox
from rect import Rect
from player import Player
from items import KeyItem

""" Key class to show interactions between game and campaign"""

class Coin(PickableNode):
    def __init__(self,hb,name='empty'):
        PickableNode.__init__(self,hb,name='empty')
        self.create_sps("coin")

    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                o2.add_score(100)
                self.taken = True
                #Remove the coin
                self.vanish()
    
    def restore(self):
        self.taken = False
        self.create_sps("coin")
    
