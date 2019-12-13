from shield import Shield
from laserBall import LaserBall
class LaserBallShield(Shield):
    def __init__(self):
        super().init()

    def generate(self):
        lb = LaserBall()
        super.generate(lb)
