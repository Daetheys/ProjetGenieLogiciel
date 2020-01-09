from mob import Mob,MobController
import sys
import os
path = os.getcwd()
sys.path.append(path + "/engine")

from controller import Autoplay
from vector import Vector
from hitbox import Hitbox
from rect import Rect
from solidPlatform import SolidPlatform

class Zombie(Mob):
    def __init__(self):
        hb = Hitbox(Rect(0,0,9,12))
        self.time_offset = 1.33
        super().__init__(hb)
        self.max_pv = 3
        self.pv = 3
        self.small = True
        self.create_sps("skeleton")
        self.sps_right = self.sps
        self.create_sps("skeleton_inverse")
        self.sps_left = self.sps
        self.animation_speed = 0.2
        self.set_state("r")
        self.controller = ZombieController(self)

        self.collide_plat = None

    def end_init(self):
        self.add_force(self.world.gravity)

    def move(self,dt):
        if self.get_speed().x >= 0:
            self.sps = self.sps_right
        else:
            self.sps = self.sps_left
        super().move(dt)

    def copy(self):
        z = Zombie()
        self.paste_in(z)

    def paste_in(self,z):
        super().paste_in(z)

    def __repr__(self):
        return "Zombie("+str(self.get_hit_box().get_world_rect())+")"

    def collide(self,o2,side,o2_side):
        super().collide(o2,side,o2_side)
        if isinstance(o2,SolidPlatform):
            self.collide_plat = o2

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
        speed = 20
        self.target.set_speedx(speed)
        if not(self.target.collide_plat is None):
            rect = self.target.collide_plat.get_hit_box().get_world_rect()
            rect_mx = rect.get_min_x()
            length = rect.get_max_x() - rect_mx
            player_x = self.target.world.player.get_position().x
            target_x = self.target.get_position().x
            move_treshold = 0.05
            block_treshold = 0.1
            print("-",target_x,rect_mx+length*0.1,rect_mx+length*0.9,player_x)
            if rect_mx+length*move_treshold < target_x < rect_mx+length*(1-block_treshold) and target_x < player_x:
                self.target.set_speedx(speed)
            elif rect_mx + length*block_treshold < target_x < rect_mx+length*(1-move_treshold) and player_x < target_x:
                self.target.set_speedx(-speed)
            else:
                self.target.set_speedx(0)
        if self.target.alive:
            self.target.move(dt)
        self.timer += 1 
        if self.timer == 50:
            self.timer = 0
            #self.jump(0.06)
