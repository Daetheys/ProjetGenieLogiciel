from engine.projectile import Projectile
from engine.controller import Controller

class LaserBall(Projectile):
    """ Vary simple projectile """
    def __init__(self):
        super().__init__()
        self.damages = 1
        self.create_sps("spike")

    def collide(self,o,side,oside):
        super().collide(o,side,oside)

class LaserBallController(Controller):
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        """ Moves the projectile """
        self.move(dt)
