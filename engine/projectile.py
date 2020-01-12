from engine.controlableNode import ControlableNode
import engine.lifeableNode
from engine.solidPlatform import SolidPlatform
from engine.hitbox import Hitbox
from engine.rect import Rect

class Projectile(ControlableNode):
    """ Projectile class """
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

    def load(self):
        pass

    def paste_in(self,p):
        super().paste_in(p)
        p.lifecollide = self.lifecollide
        p.projcollide = self.projcollide
        p.solidcollide = self.solidcollide

    def shutdown(self):
        """ Remove the projectile """
        self.set_collide(False)
        self.vanish()

    def collide(self,o,side,oside):
        """Collisions with the projectile -> will shutdown upon almost every collision dealing damages if a Lifeable is hit. Thos collisions can be modified by booleans self.lifecollide, self.projcollide, self.solidcollide"""
        if isinstance(o,engine.lifeableNode.LifeableNode) and self.lifecollide:
            self.shutdown()
        if isinstance(o,Projectile) and self.projcollide:
            self.shutdown()
        if isinstance(o,SolidPlatform) and self.solidcollide:
            self.shutdown()
