
from engine.controlableNode import ControlableNode
from engine.player import Player

from game.campaign.items import KeyItem
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
        pn = PickableNode(self.get_hit_box(),sps_name=self.sps_name)
        self.paste_in(pn)
        return pn

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


class Poison(PickableNode):
    """
    As advised by D.Baelde, all subclasses of PickableNode are flocked in this file.
    Poison class -> you need an antidote within 10 seconds"""
    def __init__(self,hb,name='poison'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):

        if o2.poisoned_timeout == 0:
            o2.poisoned_timeout = 10
        else:
            o2.take_damages(1)


class Antidote(PickableNode):
    """Antidote class -> saves you from the poison and restores 1 HP"""
    def __init__(self,hb,name='antidote'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):
        o2.add_score(400)
        o2.poisoned_timeout = 0
        if o2.pv < o2.max_pv:
            o2.pv += 1


class Coin(PickableNode):
    """ Coin class -> gives you some score"""
    def __init__(self,hb,name='coin'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):
        o2.add_score(100)


class DeadlyPotion(PickableNode):
    """ DeadlyPotion class -> kills you instantly"""
    def __init__(self,hb,name='deadlyPotion'):
        PickableNode.__init__(self,hb,name)
        self.used = False

    def upon_colliding(self,o2):
        if not self.used:
            o2.add_score(-1000)
            o2.die()
            self.used = True


    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                self.upon_colliding(o2)
                #Does not Remove the Pickable


class Key(PickableNode):
    """ Key class to show interactions between game and campaign"""
    def __init__(self,hb,name="key"):
        PickableNode.__init__(self,hb,name)
        self.key = KeyItem(name)

    def upon_colliding(self,o2):
        o2.set_inventory({self.key:1})
        o2.add_score(2000)


class Heart(PickableNode):
    """ Heart class -> adds one life to the player"""
    def __init__(self,hb,name='heart'):
        PickableNode.__init__(self,hb,name)

    def upon_colliding(self,o2):
        o2.max_pv += 1
        o2.pv += 1
        o2.add_score(800)

class RotationWorld(PickableNode):
    """ Rotates the camera """
    def __init__(self,hb,name='rotateworld'):
        super().__init__(hb,name)

    def upon_colliding(self,o2):
        self.world.camera.set_rotation_effect()
        o2.add_score(20000)
