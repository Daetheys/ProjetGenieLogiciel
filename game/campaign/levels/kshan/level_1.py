
from imports import *

class Level_1_kshan(Level):
    
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
        g.player.set_inventory({KeyItem("key_0") : 1})
        
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

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Hyborian village"],parallax=g.options["parallax"])
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
        plat_1 = SolidPlatform(Hitbox(Rect(-10,12,300,18)))
        coin_1 = Coin(Hitbox(Rect(150,-2,10,10)))
        coin_2 = Coin(Hitbox(Rect(170,-2,10,10)))
        coin_3 = Coin(Hitbox(Rect(190,-2,10,10)))
        coin_4 = Coin(Hitbox(Rect(210,-2,10,10)))
        coin_5 = Coin(Hitbox(Rect(230,-2,10,10)))
        coin_6 = Coin(Hitbox(Rect(250,-2,10,10)))
        deadly = DeadlyPotion(Hitbox(Rect(100,-2,10,10)))
        
        if not self.get_accessed():
            heart = Heart(Hitbox(Rect(280,-2,10,10)))
        else:
            heart = self.objects[-2]

        gravshield = LaserPickableShield()
        gravshield.set_position(70,0)

        zombie = Zombie()
        zombie.set_position(340,0)

        laserbot = LaserTurretBot()
        laserbot.set_position(450,-50)
        
        plat_2 = SolidPlatform(Hitbox(Rect(310,12,200,18)))
        flag = Flag(Hitbox(Rect(500,-8,10,20)))
        
        return [plat_1,plat_2,coin_1,coin_2,coin_3,coin_4,coin_5,coin_6,zombie,laserbot,heart,flag,deadly,gravshield]
