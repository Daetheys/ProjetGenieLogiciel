from projectile import Projectile
from controller import KeyboardController
class LaserBall(Projectile):
    def __init__(self):
        super().__init__()
        self.damages = 1
        self.create_sps("spike")

    def collide(self,o,side,oside):
        super().collide(o,side,oside)

class LaserBallController(KeyboardController):
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        self.move(dt)
