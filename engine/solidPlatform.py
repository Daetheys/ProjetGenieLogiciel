from controlableNode import ControlableNode
from spriteScheduler import *
import copy

class SolidPlatform(ControlableNode):
    def __init__(self,polygon):
        ControlableNode.__init__(self)
        self.set_hit_box(polygon)
        self.set_rigid_body(True)
        self.set_sps(SpriteScheduler('ex2'))
        self.get_sps().load_automaton()
        
    def copy(self):
        clas = self.__class__
        t2 = clas(self.get_hit_box())
        args = self.__dict__
        for attr in args.keys():
            setattr(t2,attr,copy.copy(getattr(self,attr)))
        return t2

    
    def __repr__(self):
        return "SolidPlatform("+str(self.get_hit_box())+")"

    def collide(self,o2):
        #print("collide")
        pass
