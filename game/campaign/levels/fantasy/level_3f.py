
from imports import *
from tools import PseudoRd

class Level_3_fantasy(Level):
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_odd2b"].show(g)
            else:
                quit_all = g.dict_dial["dial_odd2b"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_odd2abad"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_odd2a"].show(g)
        return quit_all
            
    def reward(self,g):
        g.player.set_inventory({KeyItem("elvish_poem") : 1})
        
    def check_victory(self,g,arg):
        return arg
        
    def launch(self,g):
        print("FANTASY\n")
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        print("-",self.objects)
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100*50/60

        gl = GameLevel(self.objects,player_pos,name="level_2_fantasy",parallax=g.options["parallax"],music="data/musics/Moon-ruins.ogg")
        gl.load_inventory(g.player.get_inventory())
        
        #g.launch_music(text) #too soon, create gap between music and level
        
        success = self.check_victory(g, g.launch_level(gl,None))
        pygame.event.get()#to capture inputs made during the wait
        
        if success:
            self.fun_dialogue(g,"good_end")
            if not self.get_finished():
                self.reward(g)
            self.set_finished()
        else:
            self.fun_dialogue(g,"bad_end")
        
        return success

    def create_objects(self,g):
        base = 100*2
        plats = []
        length = base*0.85+20
        height = 18
        ln = 100
        y = -5
        plats = [SolidPlatform(Hitbox(Rect(-40,y,base+length+10,height)),sps="platform_cave")]
        nx = 2*base-40
        rd = PseudoRd(23,47,1024,7)
        s = 0
        i = -1
        l = [None,20,20,None,-20,20,-20,20,-20,20]
        while s < 100:
            x = nx
            s = (x/base)*60/50*2+0.4
            if s < 38.8:
                y -= 20
            else:
                i += 1
                y += l[i%len(l)]
            if 38.0<s<39:
                plat = SolidPlatform(Hitbox(Rect(x,y,length/2,height)),sps="platform_cave")
                plats.append(plat)
                nx += base / 2
            else:
                plat = SolidPlatform(Hitbox(Rect(x,y,length,height)),sps="platform_cave")
                plats.append(plat)
                nx += base

        return plats


