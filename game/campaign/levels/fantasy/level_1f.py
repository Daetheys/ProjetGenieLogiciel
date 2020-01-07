
from imports import *
from tools import PseudoRd

class Level_1_fantasy(Level):
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_odd1b"].show(g)
            else:
                quit_all = g.dict_dial["dial_odd1b"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_odd1abad"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_odd1a"].show(g)
        return quit_all
            
    def reward(self,g):
        g.player.set_inventory({KeyItem("elvish_poem") : 1})
        
    def check_victory(self,g,arg):
        return arg
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        print("-",self.objects)
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100*110/60

        gl = GameLevel(self.objects,player_pos,name="level_1_fantasy",parallax=g.options["parallax"],music="data/musics/HolFix - Good Old Times.mp3")
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
        plats = []
        length = 85
        height = 18
        ln = 100
        y = -5
        plats = [SolidPlatform(Hitbox(Rect(-10,y,length,height)),sps="platform_cave")]
        rd = PseudoRd(23,47,1024,7)
        for i in range(1,100):
            x = i*ln-10
            y = rd.get(y-20,y+20)
            plat = SolidPlatform(Hitbox(Rect(x,y,length,height)),sps="platform_cave")
            plats.append(plat)
            if rd(0,50) == 0:
                deadly = DeadlyPotion(Hitbox(Rect(x+rd.get(0,length),y-10,10,10)))
                plats.append(deadly)

            if rd(0,15) == 0:
                zombie = Zombie()
                zombie.set_position(x+rd.get(length//5,length*4//5),y-25)
                plats.append(zombie)

            if rd(0,3) == 0:
                coin = Coin(Hitbox(Rect(x+rd(0,length),y-10-rd(0,50),10,10)))
                plats.append(coin)

        flag = Flag(Hitbox(Rect(x+length-10,y-20,10,20)))
        plats.append(flag)
        
        return plats
