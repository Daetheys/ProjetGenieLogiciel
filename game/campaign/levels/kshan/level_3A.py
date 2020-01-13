from game.campaign.levels.imports import *

class Level_3A_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan3Adv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan3A"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan3Abf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan3Agf"].show(g)
        return quit_all
        
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

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Evil Coins"],parallax=g.options["parallax"],limgpar=get_cave_bg(g),music="data/musics/Legend.mp3")
        gl.load_inventory(g.player.get_inventory())
        
        success = self.check_victory(g, g.launch_level(gl,None))
        pygame.event.get()#to capture inputs made during the wait
        
        if success:
            self.fun_dialogue(g,"good_end")
            self.set_finished()
            self.reward(g)
        else:
            self.fun_dialogue(g,"bad_end")
        
        return success
    
    def create_objects(self,g):
        plat = []
        dist = -10
        for i in range(10):
            l = (i+1)*130%200 + 50
            coin = Coin(Hitbox(Rect(dist+l//2,-10,10,10)))
            plat.append(coin)
            if i > 5:
                coin = Coin(Hitbox(Rect(dist,-30,10,10)))
                plat.append(coin)
            if i%2 == 0 and i>3:
                z = Zombie()
                z.set_position(dist+(l//2),-5)
                plat.append(z)
            plat.append(SolidPlatform(Hitbox(Rect(dist,5,l,18))))
            dist += l + 20
        flag = Flag(Hitbox(Rect(dist-10,-5,10,20)))
        plat.append(flag)

        gravshield = LaserPickableShield()
        gravshield.set_position(240,-30)
        plat.append(gravshield)
        
        return plat
