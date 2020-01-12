
from game.campaign.levels.imports import *
from game.tools.bg_creator import get_cave_bg

class Level_1_fantasy(Level):
    """ all functions are explained in the Level abstract class """
    
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

        limgpar = get_cave_bg(g)

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Midden Pass"],parallax=g.options["parallax"],music="data/musics/HolFix - Good Old Times.mp3",limgpar=limgpar)
        gl.load_inventory(g.player.get_inventory())
        
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
        x = -10
        plats = [SolidPlatform(Hitbox(Rect(x,y,100+length,height)),sps="platform_cave")]
        flag = Flag(Hitbox(Rect(x+length+100-10,y-20,10,20)))
        plats.append(flag)
        nx = -10+200
        rd = PseudoRd(23,47,1024,7)
        s = 0
        while s < 117:
            x = nx
            s = (x/100)*60/(110)
            y = rd.get(y-20,y+20)
            if s<3.9 or 31.6<s<82.7 or 100<s:
                    plat = SolidPlatform(Hitbox(Rect(x,y,length+100,height)),sps="platform_cave")
                    plats.append(plat)
                    nx += 100
            else:
                plat = SolidPlatform(Hitbox(Rect(x,y,length,height)),sps="platform_cave")
                plats.append(plat)
            if (5<s<31.6 or 82.1<s<101.3) and rd(0,30) == 1:
                deadly = DeadlyPotion(Hitbox(Rect(x+rd.get(0,length-10),y-10,10,10)))
                plats.append(deadly)

            if (5<s<31.6 or 64.5<s<101.3) and rd(0,9) == 0:
                zombie = Zombie()
                zombie.set_position(x+rd.get(length//5,length*4//5),y-15)
                plats.append(zombie)

            if rd(0,3) == 0:
                coin = Coin(Hitbox(Rect(x+rd(0,length),y-10-rd(0,50),10,10)))
                plats.append(coin)
            nx += 100

        flag = Flag(Hitbox(Rect(x+length+100-10,y-20,10,20)))
        plats.append(flag)
        
        return plats
