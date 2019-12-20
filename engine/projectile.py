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

        self.lifecollide = True
        self.projcollide = True
        self.solidcollide = True

    def copy(self):
        p = Projectile()
        self.paste_in(p)
        return p

    def paste_in(self,p):
        super().paste_in(p)
        p.lifecollide = self.lifecollide
        p.projcollide = self.projcollide
        p.solidcollide = self.solidcollide

    def shutdown(self):
        self.set_collide(False)
        self.vanish()

    def collide(self,o,side,oside):
        if isinstance(o,lifeableNode.LifeableNode) and self.lifecollide:
            print("proj life")
            self.shutdown()
        if isinstance(o,Projectile) and self.projcollide:
            print("proj collide")
            self.shutdown()
        if isinstance(o,solidPlatform.SolidPlatform) and self.solidcollide:
            print("proj plat")
            self.shutdown()
