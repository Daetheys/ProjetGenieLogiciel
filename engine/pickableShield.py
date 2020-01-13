from engine.pickableNode import PickableNode
from engine.hitbox import Hitbox
from engine.rect import Rect
from engine.laserBallShield import LaserBallShield
from engine.gravitationalBallShield import GravitationalBallShield
from engine.player import Player

class PickableShield(PickableNode):
    """ A pickable node which gives a shield """
    def __init__(self,shield,name='spike'):
        hb = Hitbox(Rect(0,0,10,10))
        PickableNode.__init__(self,hb,name)
        self.create_sps("spike")
        self.shield = shield

    def collide(self,o2,side,other_side):
        """ When hit the player gives it a shield """
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                self.shield.link_world(self.world)
                o2.add_shield(self.shield)
                self.taken = True
                #Remove the node
                self.vanish()

class GravitationalPickableShield(PickableShield):
    def __init__(self):
        s = GravitationalBallShield()
        super().__init__(s)

class LaserPickableShield(PickableShield):
    def __init__(self):
        s = LaserBallShield()
        super().__init__(s)
