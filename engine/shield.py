from controlableNode import ControlableNode
import numpy

class Shield(ControlableNodeNode):
    def __init__(self):
        super.init()
        self.speed = 10
        self.nb = 15
        self.size = 50

    def generate(self,obj):
        for i in range(self.nb):
            x = np.cos(i/self.nb*np.pi*2)*self.size
            y = np.sin(i/self.nb*np.pi*2)*self.size
            o = obj.copy()
            o.set_position(x,y)
            self.attach_children(o)
            self.world.add_node(o)

    def update(self):
        self.rotate(self.speed)
