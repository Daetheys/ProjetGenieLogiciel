from game.campaign.levels.imports import *

class Level_3B_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan3Bdv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan3B"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan3Bbf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan3Bgf"].show(g)
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

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Cloudy with a chance of Skeletons"] ,parallax=g.options["parallax"],limgpar=get_deep_forest_bg(g),music="data/musics/Boss.mp3")
        
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
            if i:
                zom = JumpingSkeleton()
                zom.set_position(dist+4,10)
                obj.append(zom)
            obj.append(SolidPlatform(Hitbox(Rect(dist,10,l,18))))
            dist += l + 20
        obj.append(Flag(Hitbox(Rect(dist-20,-15,10,20))))
        
        return obj
