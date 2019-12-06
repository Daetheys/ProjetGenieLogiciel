from controlableNode import ControlableNode

""" A controllable node is a node with a controller (an object that will catch events such as keyboard interuptions and that will call specific functions of the controllable node to move it (like a puppet)"""


class PickableNode(ControlableNode):
    """ CollideTransformable with a controller """
    def __init__(self,hb,name='empty'):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_collide(True)
        self.center_hit_box()
        self.taken = False

    def center_hit_box(self):
        self.get_hit_box().center()

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
            pass