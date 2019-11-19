from movableNode import MovableNode

class ControlableNode(MovableNode):
    """ Node with a controller """
    def __init__(self):
        super().__init__()
        self.__controller = None
        self.__actions = {"Nothing":do_nothing}

    def copy(self):
        cn = ControlableNode()
        super().__init__(cn)
        cn.set_controller(self.get_controller)
        return cn
        
    def set_controller(controller):
        self.__controller = controller

    def get_controller(self):
        return self.__controller
        
    def add_action(action,method):
        self.__actions[action] = method
        
    def execute(action):
        return self.__actions[action]
        
        
def do_nothing():
    pass
