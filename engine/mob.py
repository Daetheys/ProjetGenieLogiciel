class Mob(ControllableNode):
    def __init__(self,hb,name='zombie'):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_rigid_body(True)
        self.set_sps(SpriteScheduler(name))
        self.get_sps().load_automaton()
        self.get_sps().load_sprites()

    def copy(self):
        """ Returns the copy of this """
        sd = SolidPlatform(Hitbox(Rect(0,0,0,0)))
        self.paste_in(sd)
        return sd

    def paste_in(self,t):
        ControlableNode.paste_in(self,t)

    def __repr__(self):
        return "SolidPlatform("+str(self.get_position())+","+str(self.get_hit_box())+")"

    def collide(self,o2):
        """ Function called when this collides something else """
        pass
