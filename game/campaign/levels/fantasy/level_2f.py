
from imports import *

class Level_2_fantasy(Level):
    """ all functions are explained in the Level abstract class """
    
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
            return t*100*1/1*2

        limgpar = [("data/img/background_deep_forest/Layer_0010_1.png",0),("data/img/background_deep_forest/Layer_0009_2.png",1),("data/img/background_deep_forest/Layer_0008_3.png",2),("data/img/background_deep_forest/Layer_0007_Lights.png",3),("data/img/background_deep_forest/Layer_0006_4.png",4),("data/img/background_deep_forest/Layer_0005_5.png",5),("data/img/background_deep_forest/Layer_0004_Lights.png",6),("data/img/background_deep_forest/Layer_0003_6.png",7),("data/img/background_deep_forest/Layer_0002_7.png",8),("data/img/background_deep_forest/Layer_0001_8.png",9),("data/img/background_deep_forest/Layer_0000_9.png",10)]

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Haelgard Forest"],parallax=g.options["parallax"],music="data/musics/elves test.ogg",limgpar=limgpar)
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
        length = base*0.85
        height = 18
        ln = 100
        x = -10
        y = -5
        plats = [SolidPlatform(Hitbox(Rect(x,y,base+length+10,height)),sps="platform")]
        flag = Flag(Hitbox(Rect(x+length+100-10,y-20,10,20)))
        plats.append(flag)
        nx = 2*base
        rd = PseudoRd(23,47,1024,7)
        s = 0
        while s < 180:
            x = nx
            s = (x/base)
            y = rd.get(y-20,y+20)
            if 38<=s<39:
                plat = SolidPlatform(Hitbox(Rect(x,y,length-10,height)),sps="platform")
                plats.append(plat)
                offset = 200
                plat = SolidPlatform(Hitbox(Rect(x+base,y+offset,length+2*base,height)),sps="platform")
                plats.append(plat)
                flag = Flag(Hitbox(Rect(x+length+3*base-10,y+offset-20,10,20)))
                plats.append(flag)
                y -= 60
            else:
                plat = SolidPlatform(Hitbox(Rect(x,y,length,height)),sps="platform")
                plats.append(plat)
            if s > 42 and rd(0,20) == 1 or s > 90 and rd(0,10) == 1 or s > 180 and rd(0,5) or s > 240 and rd(0,2):
                deadly = DeadlyPotion(Hitbox(Rect(x+rd.get(0,length-10),y-10,10,10)))
                plats.append(deadly)

            if rd(0,3) == 0 and s < 42 or rd(0,10) and s < 90:
                coin = Coin(Hitbox(Rect(x+rd(0,length),y-10-rd(0,50),10,10)))
                plats.append(coin)
            nx += base

        return plats
