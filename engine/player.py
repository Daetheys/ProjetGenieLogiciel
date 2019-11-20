from controlableNode import ControlableNode
from solidePlatform import SolidPlatform

class Player(ControlableNode):
    def __init__(self):
        ControlableNode.__init__(self)
        self.set_hit_box(Hitbox(Rect(-1,-2,2,4)))
        self.set_rigid_body(True)
        self.set_sps(None)
        self.get_sps().load_automaton()
        self.get_sps().load_sprites()
        jump_strength = 5
        can_jump = False

    def jump(self):
        if self.can_jump:
            self.set_speed(self.get_speed()+Vector(0,-self.jump_strength))
            self.can_jump = False

    def allow_jump(self):
        self.can_jump = True

    def collide(self,o):
        if isinstance(o,SolidePlatform):
            self.allow_jump()
