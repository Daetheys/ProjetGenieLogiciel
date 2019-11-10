from controlableNode import ControlableNode

class SolidPlatform(ControlableNode):
    def __init__(self,polygon):
        super().__init__()
        self.set_hit_box(polygon)
        self.set_rigid_body(True)
