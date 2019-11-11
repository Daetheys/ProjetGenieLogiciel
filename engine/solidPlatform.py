from controlableNode import ControlableNode

class SolidPlatform(ControlableNode):
    def __init__(self,polygon):
        super().__init__()
        self.set_hit_box(polygon)
        self.set_rigid_body(True)

    def __repr__(self):
        return "SolidPlatform("+str(self.get_hit_box())+")"

    def collide(self,o2):
        print("collide")
