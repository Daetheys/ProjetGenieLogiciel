from controlableNode import ControlableNode
from spriteScheduler import *

class SolidPlatform(ControlableNode):
    def __init__(self,polygon):
        ControlableNode.__init__(self)
        self.set_hit_box(polygon)
        self.set_rigid_body(True)
        self.set_sps(SpriteScheduler('ex2'))
        self.get_sps().load_automaton()
        

    def __repr__(self):
        return "SolidPlatform("+str(self.get_hit_box())+")"

    def collide(self,o2):
        #print("collide")
        pass
