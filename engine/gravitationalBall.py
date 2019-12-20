from projectile import Projectile
from laserBallShield import LaserBallShield

class GravitationalBall(Projectile):
    def __init__(self):
        super().__init__()
        self.damages = 1
        self.create_sps("spike")

    def load(self):
        s = LaserBallShield()
        s.size = 8
        self.add_shield(s)

    def collide(self,o,side,oside):
        super().collide(o,side,oside)

class GravitationalBallController:
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        self.move(dt)
