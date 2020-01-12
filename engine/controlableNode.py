from engine.collideTransformable import CollideTransformable

class ControlableNode(CollideTransformable):
    """ A controllable Node is a node with a controller (an object that will catch events such as keyboard interuptions and that will call specific functions of the controllable node to move it (like a puppet)"""
    def __init__(self):
        """ CollideTransformable with a controller """
        super().__init__()
        self.controller = None
        self.world = None #Ref to a gameLevel

    def copy(self):
        """ Returns a copy of itself """
        cn = ControlableNode()
        self.paste_in(cn)
        return cn

    def paste_in(self,cn):
        """" Paste it in cn """
        CollideTransformable.paste_in(self,cn)
        cn.set_controller(self.get_controller())
        cn.link_world(self.world)

    def link_world(self,w):
        """ Set the world attribute """
        self.world = w

    def add_shield(self,s):
        """ Adds a shield [s] to the controlableNode """
        pos = self.get_position()
        s.set_position(pos.x,pos.y)
        self.world.add_node(s)
        s.generate()
        self.attach_children(s)

    def end_init(self):
        """ Will be called at the end of the initialisation of the GameLevel """
        pass

    def set_controller(self,controller):
        """ Sets the controller """
        self.controller = controller

    def get_controller(self):
        """ Returns the controller """
        return self.controller

    def collide(self,o,side,o2_side):
        """ This collides o. Sides hit are [side] for this and [o2_side] for o (top:0,right:1,bot:2,left:3) -> will be defined in gameobjects"""
        pass
