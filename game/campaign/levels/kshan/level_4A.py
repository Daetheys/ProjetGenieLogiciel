from game.campaign.levels.imports import *

class Level_4A_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan4Adv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan4A"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan4Abf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan4Agf"].show(g)
            if g.player.is_in_inventory(KeyItem("key_B")):
                quit_all = g.dict_dial["dial_kshan4gf"].show(g)   
                if not "Midden Pass" in g.save["accessible"]:
                    g.save["accessible"].append("Midden Pass") 
            else:
                quit_all = g.dict_dial["dial_kshan4bf"].show(g)
        return quit_all
        
        
    def check_victory(self,g,arg):
        return arg
        
    def reward(self,g):
        g.player.set_inventory({KeyItem("key_A"):1})
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100 #*8 to be faster (but it doesn't match the music anymore !

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Twin Turrets"],parallax=g.options["parallax"],limgpar=get_cave_bg(g),music="data/musics/Soliloquy.mp3")
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
        obj = []
        dist = -10
        for i in range(10):
            l = (i+1)*70%100 + 50
            obj.append(SolidPlatform(Hitbox(Rect(dist,(i*-8)+10,l,16))))
            if i == 7:
                laserbot = LaserTurretBot()
                laserbot.set_position(dist+(l//2),-100)
                obj.append(laserbot)
            dist += l+(i*9%13) +10
            if i > 0:
                coin = Coin(Hitbox(Rect(dist+2,(i*-8)-10,10,10)))
                obj.append(coin)
            
        for i in range(10,20):
            l = (i+1)*70%100 + 50
            obj.append(SolidPlatform(Hitbox(Rect(dist,((i-10)*12)-62,l,16))))
            if i == 12:
                las2 = LaserTurretBot()
                las2.set_position(dist+(l//2),-100)
                obj.append(las2)
            dist += l+(i*9%13) +10
            coin = Coin(Hitbox(Rect(dist+l//2,((i-10)*12)-72,10,10)))
            obj.append(coin)
            
        gps = GravitationalPickableShield()
        gps.set_position(170,-30)
        obj.append(gps)
        
        obj.append(Flag(Hitbox(Rect(dist+l//4,43,10,20))))
        obj.append(SolidPlatform(Hitbox(Rect(dist+l//4,63,16,16))))
        
        return obj
