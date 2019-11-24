from collideTransformable import CollideTransformable

class ControlableNode(CollideTransformable):
    """ Node with a controller """
    def __init__(self):
        super().__init__()
        self.controller = None
        self.__actions = {"Nothing":do_nothing}

    def copy(self):
        cn = ControlableNode()
        self.paste_in(cn)
        return cn

    def paste_in(self,cn):
        CollideTransformable.paste_in(self,cn)
        cn.set_controller(self.get_controller())
        
    def set_controller(self,controller):
        self.controller = controller

    def get_controller(self):
        return self.controller
        
    def add_action(self,action,method):
        self.__actions[action] = method

    def collide(self,o,sides,o2_sides):
        """ This collides o. Sides hit are [sides] for this and [o2_sides] for o (top:0,right:1,bot:2,left:3) """
        pass
        
    def execute(self,action):
        return self.__actions[action]
        
        
def do_nothing():
    pass
