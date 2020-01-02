from mob import Mob,MobController
import sys
import os
path = os.getcwd()
sys.path.append(path + "/engine")

from controller import Autoplay
from vector import Vector
from hitbox import Hitbox
from rect import Rect

class Zombie(Mob):
    def __init__(self):
        hb = Hitbox(Rect(0,0,12,16))
        super().__init__(hb)
        self.max_pv = 3
        self.pv = 3
        self.small = True
        self.create_sps("skeleton")
        self.animation_speed = 0.2
        self.set_state("r")
        self.controller = ZombieController(self)

    def end_init(self):
        self.add_force(self.world.gravity)

    def copy(self):
        z = Zombie()
        self.paste_in(z)

    def paste_in(self,z):
        super().paste_in(z)

    def __repr__(self):
        return "Zombie("+str(self.get_hit_box().get_world_rect())+")"

    def collide(self,o2,side,o2_side):
        super().collide(o2,side,o2_side)
        

    def die(self):
        self.set_state("d")
        super().die()

class ZombieController(MobController):
    def __init__(self,target=None):
        super().__init__()
        self.target = target
        self.timer = 0

    def execute(self,event,pressed,dt):
        super().execute(event,pressed,dt)
        self.target.set_speedx(10)
        if self.target.alive:
            self.target.move(dt)
        self.timer += 1
        if self.timer == 50:
            self.timer = 0
            self.jump(0.06)
