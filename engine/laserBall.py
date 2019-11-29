from projectile import Projectile

class LaserBall(Projectile):
    def __init__(self):
        super().init()

    def collide(self,o2):
        if isinstance(o2,Projectile):
            o2.destroy()
            self.destroy()
        if isinstance(o2,Player):
            o2.die()
