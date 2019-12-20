from mob import Mob
import sys
import os
path = os.getcwd()
sys.path.append(path + "/engine")

from controller import Autoplay
from vector import Vector
from hitbox import Hitbox
from rect import Rect
from laserBall import LaserBall


class LaserTurretBot(Mob):
    def __init__(self):
        hb = Hitbox(Rect(0,0,7,7))
        super().__init__(hb)
        self.set_rigid_body(True)
        self.max_pv = 1
        self.pv = 1
        self.small = True
        self.create_sps("Rhombus")
        self.animation_speed = 0.2
        self.controller = LaserTurretBotController(self)

    def copy(self):
        z = LaserTurretBot()
        self.paste_in(z)

    def paste_in(self,z):
        super().paste_in(z)

    def __repr__(self):
        return "LaserTurretBot("+str(self.get_hit_box().get_world_rect())+")"

    def collide(self,o2,side,o2_side):
        super().collide(o2,side,o2_side)

    def die(self):
        super().die()

class LaserTurretBotController(Autoplay):
    def __init__(self,target=None):
        super().__init__()
        self.target = target
        self.clock = 0
        self.period = 0.5

    def execute(self,event,pressed,dt):
        self.clock += dt
        if self.clock > self.period:
            self.clock -= self.period
            lb = LaserBall()
            lb.set_speed(Vector(0,40))
            (x,y) = self.target.get_position().to_tuple()
            h = lb.get_hit_box().get_world_rect().get_dimension().y
            lb.set_position(x,y+h+4)
            self.target.world.add_node(lb)
            lb.load()
        
