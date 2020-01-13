
import pygame
import json
from game.campaign.world import *
from game.campaign.level_sequence import *
from game.campaign.level import *
from game.campaign.map import *
import game.tools.creation
import game.tools.conversion
import game.tools.text_display
from shutil import copy2
from game.campaign.items import item_from_name

from game.campaign.levels.kshan.level_1 import Level_1_kshan
from game.campaign.levels.kshan.level_2 import Level_2_kshan
from game.campaign.levels.kshan.level_3A import Level_3A_kshan
from game.campaign.levels.kshan.level_4A import Level_4A_kshan
from game.campaign.levels.kshan.level_3B import Level_3B_kshan
from game.campaign.levels.kshan.level_4B_1 import Level_4B_1_kshan
from game.campaign.levels.kshan.level_4B_2 import Level_4B_2_kshan
from game.campaign.levels.fantasy.level_1f import Level_1_fantasy
from game.campaign.levels.fantasy.level_2f import Level_2_fantasy
from game.campaign.levels.fantasy.level_3f import Level_3_fantasy
from game.campaign.levels.fantasy.level_4f import Level_4_fantasy

#The Launcher class, very pure, no buttons needed
class Launcher:
    """ The Launcher class initializes as many things as possible. Notably:
    - the window (computes the biggest possible resolution, defines flip..)
    - the images (creating a dictionary)
    - the constants (used to print buttons in a pretty way)
    - the musics (initializing the pygame player, etc ..)
    - the items (creating a dictionary)
    - the characters (creating a dictionary)
    - the dialogues (creating a dictionary)
    - the strings of all languages (creating several dictionaries)
    - the world (creating all maps, levels, etc.)"""

    def __init__(self):
        self.init_window()
        self.init_images()
        self.init_constants()
        self.init_music()
        self.create_items()
        self.init_characters()
        self.load_languages(True)
        self.load_savefile()
        self.create_dialogues()
        self.create_world()
        print("The game initialized properly.")

    def init_window(self):
        """
        initializes a window, pygame graphics, and options
        returns the display window
        """
        #Redirecting stdout
        from sys import stdout as sysout
        sysout = open('doc/log.log', 'w')

        #Display
        pygame.init()
        try:
            with open("data/json/options.json","r") as file:
                self.options = json.load(file)
                #self.options["modeECRAN"]  = 0 ou FULLSCREEN

            #to test if new options have been added (by a push) to default_options
            with open("data/json/default_options.json","r") as file:
                opt = json.load(file)
            if len(self.options) < len(opt):
                self.options = opt
            #copy2("data/json/default_options.json","data/json/options.json")
        except FileNotFoundError:
            with open("data/json/default_options.json","r") as file:
                self.options = json.load(file)
            copy2("data/json/default_options.json","data/json/options.json")


        #cas de la trop faible résolution de l'écran
        i = pygame.display.Info()
        width = i.current_w
        height = i.current_h
        if width < self.options["DISPLAYSIZE_X"] or height < self.options["DISPLAYSIZE_Y"]:
                self.options["DISPLAYSIZE_Y"] = height
                self.options["DISPLAYSIZE_X"] = width
                with open("data/json/options.json","w") as f:
                    f.write(json.dumps(self.options))

        pygame.display.set_caption("CAN·A·BAELDE")
        pygame.display.set_icon(pygame.image.load("data/img/icon.ico"))
        self._fenetre = pygame.display.set_mode((self.options["DISPLAYSIZE_X"], self.options["DISPLAYSIZE_Y"]),self.options["modeECRAN"])#1920*1080 for instance
        self._fenetre.set_alpha(None) #To speed things up




    def init_images(self):
        """loads all images into self.dict_img, blits the first background"""
        #Images
        with open("data/json/img.json", "r") as read_file:
            self.dict_img = json.load(read_file,object_hook=game.tools.creation.create_img)
        #Img_transformations
        self.dict_img["img_arrow"]  = pygame.transform.smoothscale(self.dict_img["img_arrow"],(40,40))
        self.dict_img["img_garrow"]  = pygame.transform.smoothscale(self.dict_img["img_garrow"],(40,40))
        self.dict_img["img_cont_dial"]  = pygame.transform.smoothscale(self.dict_img["img_cont_dial"],(40,40))
        self.dict_img["img_end_dial"]  = pygame.transform.smoothscale(self.dict_img["img_end_dial"],(40,40))
        self.dict_img["img_inv"]  = pygame.transform.smoothscale(self.dict_img["img_inv"],(100,100))
        self.dict_img["img_inv_h"]  = pygame.transform.smoothscale(self.dict_img["white"],(100,100))
        self.dict_img["img_inv_h"].blit(self.dict_img["img_inv"], (0,0))
        self.dict_img["img_key"]  = pygame.transform.smoothscale(self.dict_img["img_key"],(64,64))
        self.dict_img["img_dial"] = pygame.transform.smoothscale(self.dict_img["img_dial"],(self.options["DISPLAYSIZE_X"],self.dict_img["img_dial"].get_height()))
        self._fenetre.blit(self.dict_img["img_background"],(0,0))
        self.flip()

    def win(self):
        """ returns the window where the game is displayed"""
        return self._fenetre

    def init_constants(self):
        """ this function initializes some constants"""
        #ces constantes sont utilisées dans la boucle principale de menu
        self.quitter_jeu = False
        self.continuer_menu =  True

        #constantes d'affichage
        self.b1xmin = self.options["DISPLAYSIZE_X"]//2 - 250
        self.b1xmax = self.options["DISPLAYSIZE_X"]//2 + 250
        self.b1ymin = 230
        self.b1ymax = 400
        self.b31xmin = self.options["DISPLAYSIZE_X"]//3-250
        self.b31xmax = self.options["DISPLAYSIZE_X"]//3+250
        self.b32xmin = 2*self.options["DISPLAYSIZE_X"]//3-250
        self.b32xmax = 2*self.options["DISPLAYSIZE_X"]//3+250
        self.yoffset = int(self.options["DISPLAYSIZE_Y"]/4.5)

        #Autres constantes
        self.max_number_scores = 10#max number of saved scores
        self.player_name = "PLAYER"#will be in options/savefile soon
        self.menu_music = "data/musics/Land of fearless.ogg"

    def load_languages(self,fst=False):
        """ this function loads all avaliable languages in self.dict_str"""
        if self.options["LANGUAGE"] == "English":
            with open("data/json/eng.json", "r", encoding="utf-8-sig") as read_file:
                self.dict_str=json.load(read_file)
        elif self.options["LANGUAGE"] == "French":
            with open("data/json/fr.json", "r", encoding="utf-8-sig") as read_file:
                self.dict_str=json.load(read_file)
        if not fst: self.update_dialogues()

    def create_items(self):
        self.dict_item = {}
        with open("data/json/items.json", "r", encoding="utf-8-sig") as read_file:
            self.dict_item = json.load(read_file, object_hook=game.tools.creation.create_item)

    def init_characters(self):
        """ creates the dictionary dict_char , from characters.json,
         and initializes self.player"""
        self.dict_char = {}
        with open("data/json/characters.json", "r", encoding="utf-8-sig") as read_file:
            self.dict_char = json.load(read_file)
            self.dict_char = game.tools.creation.create_char(self.dict_char,self.dict_img)
        self.player = self.dict_char["player"]

    def create_dialogues(self):
        """ creates the dictionary dict_dial , from dialogue.json """
        self.dict_dial = {}
        with open("data/json/dialogue.json", "r", encoding="utf-8-sig") as read_file:
            self.dict_dial = json.load(read_file)
            self.dict_dial = game.tools.creation.create_dial(self.dict_dial,self.dict_str,self.dict_char,self.dict_img)

    def create_world(self):
        """
        creates the World object, encapsulating all maps.
        Can be used on the Campaign menu
        """
        self.world = World()

        #creating the map "Kshan"
        mapkshan = Map(self.dict_img["map_kshan"],"map_kshan")

        mp_1 = Level_Sequence("kshan_1",self.options["DISPLAYSIZE_X"]*(1100/1366),self.options["DISPLAYSIZE_Y"]*(200/768),self.dict_img["img_point"],self.dict_img["img_pointf"],mapkshan)
        mp_2 = Level_Sequence("kshan_2",self.options["DISPLAYSIZE_X"]*(1000/1366),self.options["DISPLAYSIZE_Y"]*(300/768),self.dict_img["img_point"],self.dict_img["img_pointf"],mapkshan)
        mp_3A = Level_Sequence("kshan_3A",self.options["DISPLAYSIZE_X"]*(800/1366),self.options["DISPLAYSIZE_Y"]*(400/768),self.dict_img["img_point"],self.dict_img["img_pointf"],mapkshan)
        mp_4A = Level_Sequence("kshan_4A",self.options["DISPLAYSIZE_X"]*(700/1366),self.options["DISPLAYSIZE_Y"]*(330/768),self.dict_img["img_point"],self.dict_img["img_pointf"],mapkshan)
        mp_3B = Level_Sequence("kshan_3B",self.options["DISPLAYSIZE_X"]*(1050/1366),self.options["DISPLAYSIZE_Y"]*(500/768),self.dict_img["img_point"],self.dict_img["img_pointf"],mapkshan)
        mp_4B = Level_Sequence("kshan_4B",self.options["DISPLAYSIZE_X"]*(900/1366),self.options["DISPLAYSIZE_Y"]*(600/768),self.dict_img["img_point"],self.dict_img["img_pointf"],mapkshan)

        mp_1.set_levels([Level_1_kshan(self)])
        mp_2.set_levels([Level_2_kshan(self)])
        mp_3A.set_levels([Level_3A_kshan(self)])
        mp_4A.set_levels([Level_4A_kshan(self)])
        mp_3B.set_levels([Level_3B_kshan(self)])
        mp_4B.set_levels([Level_4B_1_kshan(self),Level_4B_2_kshan(self)])

        mp_1.set_childs([mp_2])
        mp_2.set_childs([mp_3A, mp_3B])
        mp_3A.set_childs([mp_4A])
        mp_3B.set_childs([mp_4B])

        map_point_list = [mp_1, mp_2, mp_3A, mp_3B, mp_4A, mp_4B]

        self.load_level_state("set_finished",map_point_list,"finished","kshan")
        self.load_level_state("set_accessible",map_point_list,"accessible","kshan")
        self.load_level_state("set_accessed",map_point_list,"accessed","kshan")

        mapkshan.set_map_points(map_point_list)

        #Create map fantasy
        mapfantasy = Map(self.dict_img["map_fantasy"],"map_fantasy",music="data/musics/Epilogue.ogg")

        mp_1 = Level_Sequence("Midden Pass",self.options["DISPLAYSIZE_X"]*(840/1600),self.options["DISPLAYSIZE_Y"]*(60/900),self.dict_img["img_point"],self.dict_img["img_pointf"],mapfantasy)
        mp_2 = Level_Sequence("Haelgard Forest",self.options["DISPLAYSIZE_X"]*(440/1600),self.options["DISPLAYSIZE_Y"]*(250/900),self.dict_img["img_point"],self.dict_img["img_pointf"],mapfantasy)
        mp_3 = Level_Sequence("Moon Ruins",self.options["DISPLAYSIZE_X"]*(940/1600),self.options["DISPLAYSIZE_Y"]*(280/900),self.dict_img["img_point"],self.dict_img["img_pointf"],mapfantasy)

        mp_1.set_levels([Level_1_fantasy(self)])
        mp_2.set_levels([Level_2_fantasy(self)])
        mp_3.set_levels([Level_3_fantasy(self),Level_4_fantasy(self)])

        mp_1.set_childs([mp_2])
        mp_2.set_childs([mp_3])

        map_point_list = [mp_1,mp_2,mp_3]

        self.load_level_state("set_finished",map_point_list,"finished","fantasy")
        self.load_level_state("set_accessible",map_point_list,"accessible","fantasy")
        self.load_level_state("set_accessed",map_point_list,"accessed","fantasy")

        mapfantasy.set_map_points(map_point_list)

        self.world.set_maps([mapkshan,mapfantasy])
    def load_level_state(self,set_fun,L,state,campaign_name):
        """ loads the state of a level in the world """
        for lvl in self.save[state]:
            if campaign_name == "kshan":
                if lvl == 'kshan_1':
                    getattr(L[0],set_fun)()
                elif lvl == 'kshan_2':
                    getattr(L[1],set_fun)()
                elif lvl == 'kshan_3A':
                    getattr(L[2],set_fun)()
                elif lvl == 'kshan_3B':
                    getattr(L[3],set_fun)()
                elif lvl == 'kshan_4B':
                    getattr(L[4],set_fun)()
                elif lvl == 'kshan_4A':
                    getattr(L[5],set_fun)()
            elif campaign_name == "fantasy":
                if lvl == 'Midden Pass':
                    getattr(L[0],set_fun)()
                elif lvl == 'Haelgard Forest':
                    getattr(L[1],set_fun)()
                elif lvl == 'Moon Ruins':
                    getattr(L[2],set_fun)()
    def saving(self):
        """ saves the game in the json file """
        self.save["inv"] = [[i.name, j] for i, j in self.player.inv.items()]
        print(self.save["inv"])
        with open("data/json/save.json","w") as f:
            f.write(json.dumps(self.save))

    def init_music(self):
        """
        initializes musical operations
        Music is currently enabled.
        A pulseaudio sink  has been added to xvfb. (done)
        """
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        #Music
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.play(-1)

    def launch_music(self,music):
        """launches the music"""
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    def update_dialogues(self):
        """ this is now an alias for create_dialogues, as map_points have currently no dialogues """
        self.create_dialogues()
        #for map in self.world.get_maps().values():
        #    for map_point in map.get_map_points():
        #        self.init_dialogues(map_point)

    def dict_str_dflt(self,char):
        """ Try to find if dict_str contains a value for the key 'char'.
        If not, it  returns the char value itself.
        This function is to be used with numbers, and strings when we do not
        know at compile time whether they will be in dict_str or not."""
        try:
            return self.dict_str[char]
        except KeyError:
            return char

    def score(self,name):
        """ Try to find if dict_score contains a value for the key 'name'.
        If not, it  returns [].
        This function is to be used with name of levels"""
        try:
            return self.dict_score[name]
        except KeyError:
            return []

    def load_savefile(self):
        """ loads all the saved data """
        try:
            with open("data/json/scores.json", "r", encoding="utf-8-sig") as read_file:
                self.dict_score = json.load(read_file)
        except FileNotFoundError:
            self.dict_score = {"level_1_kshan": [["SCHWOON", 1000000000, False], ["ALESSIO", 42000, False]]}

        try:
            with open("data/json/save.json","r") as file:
                self.save = json.load(file)
        except FileNotFoundError:
            print("Savefile not found. New savefile created !")
            with open("data/json/default_save.json","r") as file:
                self.save = json.load(file)
            copy2("data/json/default_save.json","data/json/save.json")

        self.player.inv =  game.tools.conversion.list_to_defaultdict([(item_from_name(i),j) for [i,j] in self.save["inv"]])

    def flip(self,txt=None):
        """ updates the current screen with current self.win() """
        if txt is not None:#is the SCORE usually
            game.tools.text_display.T(self.win(),txt, self.options["DISPLAYSIZE_X"]-5*len(txt),0,250,250,250,center=False)
        pygame.display.flip()

