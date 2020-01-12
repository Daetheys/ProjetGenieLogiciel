
from game.campaign.levels.imports import *

class Level_3_fantasy(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_odd3b"].show(g)
            else:
                quit_all = g.dict_dial["dial_odd3b"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_odd3abad"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_odd3a"].show(g)
        return quit_all
            
    def reward(self,g):
        g.player.set_inventory({KeyItem("elvish_poem") : 1})
        
    def check_victory(self,g,arg):
        return arg
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100*50/60*1.2

        limgpar = [(g.dict_img["cave_layer1"],1)]

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Moon Ruins"],parallax=g.options["parallax"],music="data/musics/Moon-ruins.ogg",limgpar=limgpar)
        gl.load_inventory(g.player.get_inventory())
        
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
        base = 100*1.2
        plats = []
        space = base*(1-0.87)
        height = 10
        ln = 100
        y = -5
        y1 = y
        plats = [SolidPlatform(Hitbox(Rect(-40,y,2*base+10,height)),sps="platform_cave")]
        plats.append(Flag(Hitbox(Rect(-40+2*base-10,y1-20,10,20))))
        nx = 2*base-40
        rd = PseudoRd(23,37,1024,7)
        step = 30
        l = [(-step,2),(-step,2),(-step,2),(-step,3),(-step,4)]+\
            [(-step,3),(-step,2),(-step,2),(-step,2),(-step,3),(-step,4)]+\
            [(-step,4),(step,2),(-step,2),(-step,2),(step,2),(-step,2),(step,1),(-step,2),(step,1)]+\
            [(-step,2),(step,2),(-step,2),(-step,2),(-step,2),(-step,2),(step,2),(step,2)]+\
            [(0,2),(0,2),(0,2),(0,1)]
        #True platforms
        possible = []
        done = {}
        x_tab = []
        length_tab = []
        for i,(dy,length) in enumerate(l):
            x = nx
            x_tab.append(x)
            length_tab.append(base*length-space)
            y1 = y1 + dy
            plat = SolidPlatform(Hitbox(Rect(x+space/2,y1,base*length-space,height)),sps="platform_cave")
            if dy > 0:
                possible.append((i,y1-2*step))
            else:
                possible.append((i,y1+step))
            done[str((i,y1))] = True
            plats.append(plat)
            nx += base*length
        flag = Flag(Hitbox(Rect(x+length+100-10,y1-20,10,20)))
        plats.append(flag)
        #Fake platforms
        count_i = [1]*len(l)
        for j in range(70):
            index = rd(0,len(possible))
            (i,y) = possible[index]
            if y > -step*5:
                continue
            x = x_tab[i]
            length = length_tab[i]
            try:
                done[str((x,y,length))]
            except KeyError:
                count_i[i] += 1
                if count_i[i] > 4:
                    continue
                plat = SolidPlatform(Hitbox(Rect(x+space/2,y,length,height)),sps="platform_cave")
                plats.append(plat)
                done[str((x,y,length))] = True
                if i+1 < len(l):
                    try:
                        done[(i+1,y+step)]
                    except:
                        possible.append((i+1,y+step))
                    try:
                        done[(i+1,y-step)]
                    except:
                        possible.append((i+1,y+step))
                                
        return plats


