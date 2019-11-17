from controlableNode import ControlableNode
from spriteScheduler import *
import copy

class SolidPlatform(ControlableNode):
    """ SolidPlatform of the game """
    def __init__(self,polygon,name='empty'):
        ControlableNode.__init__(self)
        self.set_hit_box(polygon)
        self.set_rigid_body(True)
        self.set_sps(SpriteScheduler(name))
        self.get_sps().load_automaton()
        self.get_sps().load_sprites()

    def copy(self):
        """ Returns the copy of this """
        clas = self.__class__
        t2 = clas(self.get_hit_box())
        args = self.__dict__
        for attr in args.keys():
            setattr(t2,attr,copy.copy(getattr(self,attr)))
        return t2


    def __repr__(self):
        return "SolidPlatform("+str(self.get_hit_box())+")"

    def collide(self,o2):
        """ Function called when this collides something else """
        #print("collide")
        pass

from vector import Vector
class Pattern(SolidPlatform):
    """ class Pattern.
    Solidplatforms in level that are moving along some pattern
    can now be considered as patterns objects. Be sure to type the right
    patternYype in the self.pt field.  """

    def __init__(self,polygon,name='empty'):
        SolidPlatform.__init__(self,polygon,name)
        self.pt = ""#patternType
        self.period = 1
        self.init_delay = 0
        self.speed = 1

    def pattern(self,t):
        """
        PatternType |What this function does
            ""      | it does not move the sprite
         "UpDown"   | the sprite moves down or up
        """
        if self.pt == "UpDown":
            if t > self.init_delay:
                if (t-self.init_delay) % self.period < self.period/2:
                    self.translate(Vector(0,self.speed))
                else:
                    self.translate(Vector(0,-self.speed))
        elif self.pt == "Square":
            if t > self.init_delay:
                if (t-self.init_delay) % self.period < self.period/4:
                    self.translate(Vector(0,self.speed))
                elif (t-self.init_delay) % self.period < self.period/2:
                    self.translate(Vector(self.speed,0))
                elif (t-self.init_delay) % self.period < 3*self.period/4:
                    self.translate(Vector(0,-self.speed))
                else:
                    self.translate(Vector(-self.speed,0))

