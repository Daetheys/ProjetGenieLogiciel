from engine.shield import Shield
from engine.laserBall import LaserBall

class LaserBallShield(Shield):
    def __init__(self):
        super().__init__()
        self.size = 15
        self.nb = 10
        self.speed = 10

    def generate(self):
        lb = LaserBall()
        lb.solidcollide = False
        super().generate(lb)
