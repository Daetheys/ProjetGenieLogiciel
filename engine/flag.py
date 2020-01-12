from engine.controlableNode import ControlableNode
from engine.player import Player

class Flag(ControlableNode):
    def __init__(self,hb):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_collide(True)
        self.center_hit_box()
        self.create_sps("red_flag")

    def center_hit_box(self):
        """ Centers the hit box (detail of physics) """
        self.get_hit_box().center()

    def copy(self):
        """ Returns a copy of itself """
        f = Flag()
        self.paste_in(f)
        return f

    def paste_in(self,f):
        """" Paste it in cn """
        Controlable.paste_in(self,f)

    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            o2.add_score(o2.pv * 1000)
            o2.world.win()
