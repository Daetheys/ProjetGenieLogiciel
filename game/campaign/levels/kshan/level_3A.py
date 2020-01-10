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
        elif arg == "bad_end_1":
            quit_all = g.dict_dial["dial_kshan3Abf1"].show(g)
        elif arg == "bad_end_2":
            quit_all = g.dict_dial["dial_kshan3Abf2"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan3Agf"].show(g)
        return quit_all
            
    def reward(self,g):
        self.key.possessed = True
        
    def check_victory(self,g,arg):
        if arg and g.player.is_in_inventory(KeyItem(self.key.sps_name)):
            return True
        return False
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100 #*8 to be faster (but it doesn't match the music anymore !

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Key To Success"],parallax=g.options["parallax"])
        gl.load_inventory(g.player.get_inventory())
        
        alive = g.launch_level(gl,None)
        success = self.check_victory(g, alive)
        pygame.event.get()#to capture inputs made during the wait
        
        if success:
            self.fun_dialogue(g,"good_end")
            self.set_finished()
            self.reward(g)
        else:
            if alive:
                self.fun_dialogue(g,"bad_end_2")
            else:
                if self.key.taken and not self.key.possessed:
                    g.player.set_inventory({KeyItem(self.key.sps_name):0})
                    self.key.taken = False
                    self.key.unvanish(self.key.sps_name)
                self.fun_dialogue(g,"bad_end_1")
        
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
        if not self.get_accessed():
            self.key = Key(Hitbox(Rect(dist+300,-38,4,4)),"key")
        plat.append(self.key)
        plat.append(Coin(Hitbox(Rect(dist+100,-42,10,10))))
        z4 = Zombie()
        z4.set_position(dist+110,-30)
        dist += 525
        for i in range(17):
            l = (i+5)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,10,l,18))))
            if i != 13 and i != 2:
                plat.append(Coin(Hitbox(Rect(dist+20,-8,10,10))))
            else:
                dp = DeadlyPotion(Hitbox(Rect(dist+20,-4,10,10)))
                plat.append(dp)
            dist += l + 20
        flag = Flag(Hitbox(Rect(dist-20,-20,10,20)))

        zombie = Zombie()
        zombie.set_position(132,0)
        z2 = Zombie()
        z2.set_position(232,-2)
        z3 = Zombie()
        z3.set_position(525,-2)
        
        return plat + [zombie,z2,z3,z4,flag] 
 
