from controlableNode import ControlableNode
from player import Player

class Flag(ControlableNode):
    def __init__(self,hb):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_collide(True)
        self.center_hit_box()
        self.create_sps("red_flag")

    def center_hit_box(self):
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
            o2.world.win()