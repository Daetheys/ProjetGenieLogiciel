from engine.shield import Shield
from engine.laserBall import LaserBall

class LaserBallShield(Shield):
    """ Very simple shield """
    def __init__(self):
        super().__init__()
        self.size = 15 #Size of the shield (distance between the center and projectiles)
        self.nb = 10 #Number of projectiles
        self.speed = 10 #Speed of projectiles

    def generate(self):
        """ Generate the shield """
        lb = LaserBall()
        lb.solidcollide = False
        super().generate(lb)
