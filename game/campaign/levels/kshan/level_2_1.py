from game.campaign.levels.imports import *

class Level_2_1_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan2_1dv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan2_1"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan2_1bf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan2_1gf"].show(g)
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

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Twin Turrets"],parallax=g.options["parallax"])
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
            l = (i+1)*70%100 + 50
            coin = Coin(Hitbox(Rect(dist+l//2,-10,10,10)))
            plat.append(coin)
            if i > 5:
                coin = Coin(Hitbox(Rect(dist,-30,10,10)))
                plat.append(coin)
            plat.append(SolidPlatform(Hitbox(Rect(dist,5,l,18))))
            dist += l + 20
        flag = Flag(Hitbox(Rect(dist-10,-5,10,20)))

        gravshield = LaserPickableShield()
        gravshield.set_position(120,5)
        laserbot = LaserTurretBot()
        laserbot.set_position(450,-50)
        las2 = LaserTurretBot()
        las2.set_position(850,-50)

        return plat+[gravshield,laserbot,las2,flag]
