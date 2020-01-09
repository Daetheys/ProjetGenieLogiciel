from controlableNode import ControlableNode
from hitbox import Hitbox
from rect import Rect
from controller import Controller
import numpy as np

class Shield(ControlableNode):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.nb = 15
        self.size = 20
        hb = Hitbox(Rect(0,0,1,1))
        self.set_hit_box(hb)
        self.set_controller(ShieldController(self))
        self.vanish()

    def generate(self,obj):
        for i in range(self.nb):
            x = np.cos(i/self.nb*np.pi*2)*self.size
            y = np.sin(i/self.nb*np.pi*2)*self.size
            o = obj.copy()
            pos = self.get_position()
            o.set_position(x+pos.x,y+pos.y)
            self.attach_children(o)
            self.world.add_node(o)
            o.load()

    def update(self,dt):
        self.rot(self.speed)

class ShieldController(Controller):
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        self.target.update(dt)
