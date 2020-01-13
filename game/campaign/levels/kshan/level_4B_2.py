from game.campaign.levels.imports import *

class Level_4B_2_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan4B_2dv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan4B_2"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan4B_2bf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan4B_2gf"].show(g)
            if g.player.is_in_inventory(KeyItem("key_A")):
                quit_all = g.dict_dial["dial_kshan4gf"].show(g)
                if not "Midden Pass" in g.save["accessible"]:
                    g.save["accessible"].append("Midden Pass")
                    g.world.get_map("map_fantasy").get_map_point("Midden Pass").set_accessible()
            else:
                quit_all = g.dict_dial["dial_kshan4bf"].show(g)
        return quit_all
        
    def reward(self,g):
        g.player.set_inventory({KeyItem("key_B"):1})
        
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

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Grave Forest"],parallax=g.options["parallax"],limgpar=get_demon_woods_bg(g),music="data/musics/Boss2.mp3")
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
        """ creates all objects in the level. """
        plat = []
        dist = -10
        for i in range(10):
            l = (i+1)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,10,l,18))))
            dist += l + 20
        plat.append(SolidPlatform(Hitbox(Rect(dist,-6,500,24))))
        plat.append(Coin(Hitbox(Rect(dist+100,-42,10,10))))
        z4 = Zombie()
        z4.set_position(dist+110,-30)
        rw = RotationWorld(Hitbox(Rect(dist+180,-65,10,10)))
        dist += 525
        for i in range(17):
            l = (i+5)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,10,l,18))))
            if i != 13 and i != 2:
                plat.append(Coin(Hitbox(Rect(dist+20,-8,10,10))))
            else:
                dp = DeadlyPotion(Hitbox(Rect(dist+25,-4,10,10)))
                plat.append(dp)
            dist += l + 20
        flag = Flag(Hitbox(Rect(dist-20,-20,10,20)))

        zombie = Zombie()
        zombie.set_position(132,0)
        z2 = Zombie()
        z2.set_position(232,-2)
        z3 = Zombie()
        z3.set_position(525,-2)
        
        return plat + [zombie,z2,z3,z4,flag,rw] 
 
