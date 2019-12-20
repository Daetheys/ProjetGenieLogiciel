from lifeableNode import LifeableNode
import player

class Mob(LifeableNode):
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
        if isinstance(o2,player.Player): #Mobs cannot collide more than once with player
            self.die()
            self.set_collide(False) #So that player can continue to run
            o2.add_score(10)

    def die(self):
        super().die()
