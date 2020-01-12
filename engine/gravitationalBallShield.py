from engine.shield import Shield
from engine.gravitationalBall import GravitationalBall

class GravitationalBallShield(Shield):
    def __init__(self):
        super().__init__()
        self.size = 15
        self.nb = 3
        self.size = 25

    def generate(self):
        """ Generate the shield """
        lb = GravitationalBall(self.world)
        lb.solidcollide = False
        super().generate(lb)
