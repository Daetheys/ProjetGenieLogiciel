from controlableNode import ControlableNode
import lifeableNode
import solidPlatform
from hitbox import Hitbox
from rect import Rect

class Projectile(ControlableNode):
    def __init__(self):
        super().__init__()
        self.damages = 1
        hb = Hitbox(Rect(0,0,4,4))
        self.set_hit_box(hb)
        self.set_collide(True)

    def shutdown(self):
        self.vanish()

    def collide(self,o,side,oside):
        print(o)
        if isinstance(o,lifeableNode.LifeableNode):
            print("life")
            self.shutdown()
        if isinstance(o,Projectile):
            self.shutdown()
        if isinstance(o,solidPlatform.SolidPlatform):
            self.shutdown()
