from imports import *

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
                quit_all = g.dict_dial["dial_kshan4f"].show(g)   
                if not "Midden Pass" in g.save["accessible"]:
                    g.save["accessible"].append("Midden Pass")             
        return quit_all
            
    def reward(self,g):
        g.player.set_inventory({KeyItem("key_A"):1})
        
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

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Grave Forest"],parallax=g.options["parallax"])
        
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
        h = 10
        for i in range(20):
            l = (i+1)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,h,l,16))))
            h += i*17%23 - 10
            dist += l+(i*9%13) +10
        flag = Flag(Hitbox(Rect(dist-20,-13,10,20)))
        
        gps = GravitationalPickableShield()
        gps.set_position(70,0)        
        ht = Heart(Hitbox(Rect(310,12,10,10)))
        ht.set_position(700,-30)
        laserbot = LaserTurretBot()
        laserbot.set_position(450,-40)
        zb = Zombie()
        zb.set_position(650,-30)
        z2 = Zombie()
        z2.set_position(850,-20)
        z3 = Zombie()
        z3.set_position(550,-20)
        return plat+[gps,ht,laserbot,zb,z2,z3,flag]
