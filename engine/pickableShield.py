from pickableNode import PickableNode
from hitbox import Hitbox
from rect import Rect
from laserBallShield import LaserBallShield
from gravitationalBallShield import GravitationalBallShield
from player import Player

class PickableShield(PickableNode):
    def __init__(self,shield,name='empty'):
        hb = Hitbox(Rect(0,0,10,10))
        PickableNode.__init__(self,hb,sps_name='empty')
        self.create_sps("spike")
        self.shield = shield

    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                self.shield.link_world(self.world)
                o2.add_shield(self.shield)
                self.taken = True
                #Remove the coin
                self.vanish()

class GravitationalPickableShield(PickableShield):
    def __init__(self):
        s = GravitationalBallShield()
        super().__init__(s)

class LaserPickableShield(PickableShield):
    def __init__(self):
        s = LaserBallShield()
        super().__init__(s)
