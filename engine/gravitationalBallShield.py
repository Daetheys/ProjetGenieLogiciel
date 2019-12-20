from shield import Shield
from gravitationalBall import GravitationalBall

class GravitationalBallShield(Shield):
    def __init__(self):
        super().__init__()
        self.size = 15
        self.nb = 10

    def generate(self):
        lb = GravitationalBall(self.world)
        lb.solidcollide = False
        super().generate(lb)
