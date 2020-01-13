from game.campaign.levels.imports import *

class Level_2_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_accessed():
                quit_all = g.dict_dial["dial_kshan2_2dv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan2_2"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan2_2bf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan2_2gf"].show(g)
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

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Grave Forest"],parallax=g.options["parallax"],limgpar=get_demon_woods_bg(g),music="data/musics/cool.mp3")
        
        
        alive = g.launch_level(gl,None)
        success = self.check_victory(g, alive)
        pygame.event.get()#to capture inputs made during the wait
        
        if success:
            self.fun_dialogue(g,"good_end")
            self.set_finished()
            self.reward(g)
        else:
            if alive:
                self.fun_dialogue(g,"bad_end")
            else:
                if self.key.taken and not self.key.possessed:
                    g.player.set_inventory({KeyItem(self.key.sps_name):0})
                    self.key.taken = False
                    self.key.unvanish(self.key.sps_name)
                self.fun_dialogue(g,"bad_end")
        
        return success
    
    def create_objects(self,g):
        plat = []
        dist = -10
        h = 10
        for i in range(20):
            l = (i+1)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,h,l,16))))
            if i%7 == 6:
                deadly = DeadlyPotion(Hitbox(Rect(dist+(l/2)-5,h-10,10,10)))
                plat.append(deadly)
            if i%11 == 4:
                heart = Heart(Hitbox(Rect(dist+(l/2)-5,h-14,10,10)))
                plat.append(heart)
            if i == 17:
                if not self.get_accessed():
                    self.key = Key(Hitbox(Rect(dist+(l/2)-5,h-40,4,4)),"key")
                plat.append(self.key) 
            h += i*17%23 - 10
            dist += l+(i*9%13) +10
            
        flag = Flag(Hitbox(Rect(dist-20,-13,10,20)))
        plat.append(flag)

        return plat
