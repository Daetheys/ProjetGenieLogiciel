from game.campaign.levels.imports import *
from game.level_generation.level_generator import generate_level

class Level_4_fantasy(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_odd4b"].show(g)
            else:
                quit_all = g.dict_dial["dial_odd4b"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_odd4abad"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_odd4a"].show(g)
        return quit_all
            
    def reward(self,g):
        pass
        
    def check_victory(self,g,arg):
        return arg
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100*160/60

        limgpar = [(g.dict_img["red_layer1"],0),(g.dict_img["red_layer2"],1),(g.dict_img["red_layer3"],2),(g.dict_img["red_layer4"],3)]

        gl = generate_level("data/musics/seal.ogg",name_of_level=g.dict_str["Demon Woods"],limgpar=limgpar)
        
        if len(gl.objects) <= 650: #It may fail to build it the first time but rarely twice in a row
            gl = generate_level("data/musics/seal.ogg",name_of_level=g.dict_str["Demon Woods"],limgpar=limgpar)
            if len(gl.objects) <= 650:
                print("BUG")
                pass
        gl.load_inventory(g.player.get_inventory())
        gl.camera.set_rotation_effect()
        gl.camera.remove_rotation_effect = False
        
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
