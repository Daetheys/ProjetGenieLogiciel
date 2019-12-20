from shield import Shield
from gravitationalBall import GravitationalBall

class GravitationalBallShield(Shield):
    def __init__(self):
        super().__init__()
        self.size = 15
        self.nb = 3
        self.size = 25

    def generate(self):
        print("--",self.world)
        lb = GravitationalBall(self.world)
        lb.solidcollide = False
        super().generate(lb)
