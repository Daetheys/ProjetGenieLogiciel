import pygame
import json
from world import *
#from map_point import *
from mapDisplayer import *
from level_sequence import *
from level import *
from map import *
import tools
from shutil import copy2

#The Game class, very pure, no buttons needed
class Game:

    def __init__(self):
        self.init_game()
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

    def init_game(self):
        """
        initializes a game,
        returns the display window
        """
        #Display
        pygame.init()

        try:
            with open("data/json/options.json","r") as file:
                self.options = json.load(file)
                #self.options["modeECRAN"]  = 0 ou FULLSCREEN
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
        self._fenetre = pygame.display.set_mode((self.options["DISPLAYSIZE_X"], self.options["DISPLAYSIZE_Y"]),self.options["modeECRAN"])#1920*1080

    def init_images(self):
        """loads all images into self.dict_img, blits the first background"""
        #Images
        with open("data/json/img.json", "r") as read_file:
            self.dict_img = json.load(read_file,object_hook=tools.create_img)
        #Img_transformations
        self.dict_img["img_arrow"]  = pygame.transform.smoothscale(self.dict_img["img_arrow"],(40,40))
        self.dict_img["img_garrow"]  = pygame.transform.smoothscale(self.dict_img["img_garrow"],(40,40))
        self.dict_img["img_cont_dial"]  = pygame.transform.smoothscale(self.dict_img["img_cont_dial"],(40,40))
        self.dict_img["img_end_dial"]  = pygame.transform.smoothscale(self.dict_img["img_end_dial"],(40,40))
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
            self.dict_item = json.load(read_file, object_hook=tools.create_item)

    def init_characters(self):
        self.dict_char = {}
        with open("data/json/characters.json", "r", encoding="utf-8-sig") as read_file:
            self.dict_char = json.load(read_file)
            self.dict_char = tools.create_char(self.dict_char,self.dict_img)
        self.player = self.dict_char["player"]

    def create_dialogues(self):
        self.dict_dial = {}
        with open("data/json/dialogue.json", "r", encoding="utf-8-sig") as read_file:
            self.dict_dial = json.load(read_file)
            self.dict_dial = tools.create_dial(self.dict_dial,self.dict_str,self.dict_char,self.dict_img)

    def create_world(self):
        """
        creates the World object, encapsulating all maps.
        Can be used on the Campaign menu
        """
        self.world = World()

        #creating the map "Kshan"
        mapkshan = Map(self.dict_img["map_kshan"],"map_kshan")

        mp_1 = Level_Sequence("kshan_1",200,200,self.dict_img["img_point"],self.dict_img["img_pointf"])
        mp_2 = Level_Sequence("kshan_2",400,200,self.dict_img["img_point"],self.dict_img["img_pointf"])
        mp_3A = Level_Sequence("kshan_3A",200,400,self.dict_img["img_point"],self.dict_img["img_pointf"])
        mp_4A = Level_Sequence("kshan_4A",200,600,self.dict_img["img_point"],self.dict_img["img_pointf"])
        mp_3B = Level_Sequence("kshan_3B",400,400,self.dict_img["img_point"],self.dict_img["img_pointf"])
        mp_4B = Level_Sequence("kshan_4B",400,600,self.dict_img["img_point"],self.dict_img["img_pointf"])

        self.init_dialogues(mp_1)
        self.init_dialogues(mp_2)
        self.init_dialogues(mp_3A)
        self.init_dialogues(mp_4A)
        self.init_dialogues(mp_3B)
        self.init_dialogues(mp_4B)

        mp_1.set_levels([Boss_Level()])
        mp_2.set_levels([Random_Level(),Boss_Level()])
        mp_3A.set_levels([Boss_Level()])
        mp_4A.set_levels([Boss_Level()])
        mp_3B.set_levels([Boss_Level()])
        mp_4B.set_levels([Boss_Level()])

        mp_1.set_childs([mp_2])
        mp_2.set_childs([mp_3A, mp_3B])
        mp_3A.set_childs([mp_4A])
        mp_3B.set_childs([mp_4B])

        mp_1.set_accessible()

        mapkshan.set_map_points([mp_1, mp_2, mp_3A, mp_3B, mp_4A, mp_4B])



        self.world.set_maps([mapkshan])

    def init_dialogues(self,mp):
        if mp.name == "kshan_1":
            mp.set_start_dialogue(self.dict_dial["dial_kshan1"])
            mp.set_end_dialogue(self.dict_dial["dial_kshan1f"])
        elif mp.name == "kshan_2":
            mp.set_start_dialogue(self.dict_dial["dial_kshan2"])
            mp.set_end_dialogue(self.dict_dial["dial_kshan2f"])
        elif mp.name == "kshan_3A":
            mp.set_start_dialogue(self.dict_dial["dial_kshan3A"])
            mp.set_end_dialogue(self.dict_dial["dial_kshan3Af"])
        elif mp.name == "kshan_4A":
            mp.set_start_dialogue(self.dict_dial["dial_kshan4A"])
            mp.set_end_dialogue(self.dict_dial["dial_kshan4Af"])
        elif mp.name == "kshan_3B":
            mp.set_start_dialogue(self.dict_dial["dial_kshan3B"])
            mp.set_end_dialogue(self.dict_dial["dial_kshan3Bf"])
        elif mp.name == "kshan_4B":
            mp.set_start_dialogue(self.dict_dial["dial_kshan4B"])
            mp.set_end_dialogue(self.dict_dial["dial_kshan4Bf"])

    def init_music(self):
        """
        initializes musical operations
        Music is currently disabled.
        Please add a pulseaudio sink to xvfb before activating it. (done)
        """
        pygame.mixer.init()
        #Music
        pygame.mixer.music.load("data/tests_musique/test.mp3")
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.play(-1)

    def launch_music(self,music):
        """launches the music"""
        pygame.mixer.music.load(music)
        #pygame.mixer.music.fadeout(500)
        pygame.mixer.music.play(-1)


    def update_dialogues(self):
        self.create_dialogues()
        for map in self.world.get_maps().values():
            for map_point in map.get_map_points():
                self.init_dialogues(map_point)

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
        with open("data/json/scores.json", "r", encoding="utf-8-sig") as read_file:
            self.dict_score = json.load(read_file)

            #for sc in self.score:
            #    self.score[sc] = self.score[sc]

    def flip(self,txt=None):
        if txt is not None:#is the SCORE usually
            tools.T(self.win(),txt, self.options["DISPLAYSIZE_X"]-5*len(txt),0,250,250,250,center=False)
        pygame.display.flip()

