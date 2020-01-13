
from game.campaign.levels.imports import *

class Level_1_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan1dv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan1"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan1bf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan1gf"].show(g)
        return quit_all
            
    def reward(self,g):
        g.player.set_inventory({KeyItem("key_0") : 1, Consommable("Apple") : 2})
        
    def check_victory(self,g,arg):
        return arg
        
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100 #*8 to be faster (but it doesn't match the music anymore !
        limgpar = get_demon_woods_bg(g)

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Hyborian Village"],parallax=g.options["parallax"],limgpar=get_demon_woods_bg(g),music="data/musics/xeon5.ogg")
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
        
        obj = []
        dist = -10
        
        for i in range(10):
            plat = SolidPlatform(Hitbox(Rect(dist,12,120,18)))
            if i%2 == 0:
                c1 = Coin(Hitbox(Rect(dist+30,-2,10,10)))
                c2 = Coin(Hitbox(Rect(dist+50,-2,10,10)))
                c3 = Coin(Hitbox(Rect(dist+70,-2,10,10)))
                obj += [c1,c2,c3]
            obj.append(plat)
            dist += 140
            if i<9:
                coin = Coin(Hitbox(Rect(dist-15,-25,10,10)))
                obj.append(coin)


        flag = Flag(Hitbox(Rect(dist-30,-8,10,20)))
        obj.append(flag)
        
        return obj
