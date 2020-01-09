import sys
import os
path = os.getcwd()
path += "/engine"
sys.path.append(path)

from controlableNode import ControlableNode
from items import KeyItem
from player import Player
""" A controllable node is a node with a controller (an object that will catch events such as keyboard interuptions and that will call specific functions of the controllable node to move it (like a puppet)"""


class PickableNode(ControlableNode):
    """ CollideTransformable with a controller """
    def __init__(self,hb,sps_name="empty"):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_collide(True)
        self.center_hit_box()
        self.taken = False
        self.possessed = False
        self.create_sps(sps_name)
        self.sps_name = sps_name

    def copy(self):
        """ Returns a copy of itself """
        pn = PickableNode()
        self.paste_in(pn)
        return cn

    def paste_in(self,pn):
        """" Paste it in pn """
        Controlable.paste_in(self,pn)

    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                self.upon_colliding(o2)
                self.taken = True
                #Remove the Pickable
                self.vanish()

"""
As advised by D.Baelde, all subclasses of PickableNode are flocked in this file.
Poison class -> you need an antidote within 10 seconds"""

class Poison(PickableNode):
    def __init__(self,hb,name='poison'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):

        if o2.poisoned_timeout == 0:
            o2.poisoned_timeout = 10
        else:
            o2.take_damages(1)

"""Antidote class -> saves you from the poison and restores 1 HP"""

class Antidote(PickableNode):
    def __init__(self,hb,name='antidote'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):
        o2.add_score(400)
        o2.poisoned_timeout = 0
        if o2.pv < o2.max_pv:
            o2.pv += 1

""" Coin class -> gives you some score"""

class Coin(PickableNode):
    def __init__(self,hb,name='coin'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):
        o2.add_score(100)

""" DeadlyPotion class -> kills you instantly"""

class DeadlyPotion(PickableNode):
    def __init__(self,hb,name='deadlyPotion'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):
        o2.add_score(-1000)
        o2.die()


    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                self.upon_colliding(o2)
                #Does not Remove the Pickable
                #self.vanish()

""" Key class to show interactions between game and campaign"""

class Key(PickableNode):
    def __init__(self,hb,name="key"):
        PickableNode.__init__(self,hb,name)
        self.key = KeyItem(name)

    def upon_colliding(self,o2):
        o2.set_inventory({self.key:1})
        o2.add_score(2000)

""" Heart class -> adds one life to the player"""

class Heart(PickableNode):
    def __init__(self,hb,name='heart'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):
        o2.max_pv += 1
        o2.pv += 1
        o2.add_score(800)