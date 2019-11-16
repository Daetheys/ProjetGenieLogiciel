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
        self.init_characters()
        self.load_languages(True)
        self.create_dialogues()
        self.create_world()
        print("The game initialized properly.")

    def init_game(self):
        """
        initializes a game,
        returns the display window
        """
        #Display
        try:
            with open("data/json/options.json","r") as file:
                self.options = json.load(file)
                #self.options["modeECRAN"]  = 0 ou FULLSCREEN
        except FileNotFoundError:
            with open("data/json/default_options.json","r") as file:
                self.options = json.load(file)
            copy2("data/json/default_options.json","data/json/options.json")

        pygame.init()
        #pygame.mixer.init() music is disabled
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
        pygame.display.flip()

    def win(self):
        """ returns the window where the game is displayed"""
        return self._fenetre

    def init_constants(self):
        """ this function initializes some constants"""
        self.quitter_jeu = False
        self.continuer_menu =  True
        self.b1xmin = self.options["DISPLAYSIZE_X"]//2 - 250
        self.b1xmax = self.options["DISPLAYSIZE_X"]//2 + 250
        self.b1ymin = 230
        self.b1ymax = 400
        self.b31xmin = self.options["DISPLAYSIZE_X"]//3-250
        self.b31xmax = self.options["DISPLAYSIZE_X"]//3+250
        self.b32xmin = 2*self.options["DISPLAYSIZE_X"]//3-250
        self.b32xmax = 2*self.options["DISPLAYSIZE_X"]//3+250
        self.yoffset = int(self.options["DISPLAYSIZE_Y"]/4.5)

    def load_languages(self,fst=False):
        """ this function loads all avaliable languages in self.dict_str"""
        if self.options["LANGUAGE"] == "English":
            with open("data/json/eng.json", "r", encoding="utf-8-sig") as read_file:
                self.dict_str=json.load(read_file)
        elif self.options["LANGUAGE"] == "French":
            with open("data/json/fr.json", "r", encoding="utf-8-sig") as read_file:
                self.dict_str=json.load(read_file)
        if not fst: self.update_dialogues()

    def init_characters(self):
        self.dict_char = {}
        with open("data/json/characters.json", "r", encoding="utf-8-sig") as read_file:
            self.dict_char = json.load(read_file)
            self.dict_char = tools.create_char(self.dict_char,self.dict_img)

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
        mp = Level_Sequence("test",200,200,self.dict_img["img_point"],self.dict_img["img_pointf"])
        self.init_dialogues(mp)
        mp.is_accessible()
        mp.set_levels([Boss_Level()])
        mapkshan.set_map_points([mp])

        self.world.set_maps([mapkshan])

    def init_dialogues(self,mp):
        if mp.name == "test":
            mp.set_start_dialogue(self.dict_dial["dial_test"])
            mp.set_end_dialogue(self.dict_dial["dial_testf"])

    def init_music(self):
        """
        initializes musical operations
        Music is currently disabled.
        Please add a pulseaudio sink to xvfb before activating it.
        """
        pass
        #Music
        #pygame.mixer.music.load(music_menu)
        #pygame.mixer.music.fadeout(500)
        #pygame.mixer.music.play(-1)

    def update_dialogues(self):
        self.create_dialogues()
        for map in self.world.get_maps().values():
            for map_point in map.get_map_points():
                self.init_dialogues(map_point)
