from engine.jumpableNode import JumpableNode,JumpableController
import engine.player

class Mob(JumpableNode):
    def __init__(self,hb):
        super().__init__()
        self.set_hit_box(hb)
        self.set_rigid_body(True)
        self.damages = 1 #Damages by hitting the mob

    def copy(self):
        """ Returns the copy of this """
        sd = SolidPlatform(Hitbox(Rect(0,0,0,0)))
        self.paste_in(sd)
        return sd

    def paste_in(self,t):
        ControlableNode.paste_in(self,t)

    def __repr__(self):
        return "SolidPlatform("+str(self.get_position())+","+str(self.get_hit_box())+")"

    def collide(self,o2,sides,o2_sides):
        """ Function called when this collides something else """
        super().collide(o2,sides,o2_sides)
        if isinstance(o2,engine.player.Player): #Mobs cannot collide more than once with player
            self.die()
            self.set_collide(False) #So that player can continue to run
            o2.add_score(10)

    def die(self):
        super().die()

class MobController(JumpableController):
    """ Controller for a Mob """
    def __init__(self,target=None):
        super().__init__(target=target)
        self.jump_time = 0

    def jump(self,strengh):
        """ Strengh of 1 is a jump similar to the max jump of player """
        self.jump_time = strengh

    def execute(self,event,pressed,dt):
        #print(self.jump_time)
        if self.jump_time > 0:
            self.jump_time = max(0,self.jump_time-dt)
            self.target.start_jump()
        else:
            self.target.stop_jump()
        super().execute(event,pressed,dt)
