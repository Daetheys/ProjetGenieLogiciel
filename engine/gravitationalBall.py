from engine.projectile import Projectile
from engine.laserBallShield import LaserBallShield
from engine.controller import Controller

class GravitationalBall(Projectile):
    def __init__(self,world):
        super().__init__()
        self.damages = 1
        self.create_sps("spike")
        self.link_world(world)
        self.solidcollide = False
        self.speed = 5

    def copy(self):
        gb = GravitationalBall(self.world)
        self.paste_in(gb)
        return gb

    def paste_in(self,gb):
        gb.load()

    def load(self):
        """ Load it shield """
        s = LaserBallShield()
        s.size = 10
        s.nb = 5
        self.add_shield(s)

    def collide(self,o,side,oside):
        super().collide(o,side,oside)

class GravitationalBallController(Controller):
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        """ Moves the projectile """
        self.move(dt)
