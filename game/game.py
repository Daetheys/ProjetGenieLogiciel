import pygame
import json
from world import *
#from map_point import *
from mapDisplayer import *
from level_sequence import *
from map import *
from tools import *

#The Game class, very pure, no buttons needed
class Game:

    def __init__(self):
        self.init_game()
        self.init_images()
        self.init_constants()
        self.init_music()
        self.load_languages()
        self.create_world()
        print("The game initialized properly")

    def init_game(self):
        """
        initializes a game,
        returns the display window
        """
        #Display
        with open("data/json/options.json","r") as file:
            self.options = json.load(file)
            #self.options["modeECRAN"]  = 0 ou FULLSCREEN
        pygame.init()
        #pygame.mixer.init() music is disabled
        pygame.display.set_caption("CAN·A·BAELDE")
        pygame.display.set_icon(pygame.image.load("data/img/icon.ico"))
        self._fenetre = pygame.display.set_mode((self.options["DISPLAYSIZE_X"], self.options["DISPLAYSIZE_Y"]),self.options["modeECRAN"])#1920*1080

    def init_images(self):
        """loads all images into self.dict_img, blits the first background"""
        #Images
        with open("data/json/img.json", "r") as read_file:
            self.dict_img = json.load(read_file,object_hook=create_img)
        #Img_transformations
        self.dict_img["img_arrow"]  = pygame.transform.smoothscale(self.dict_img["img_arrow"],(40,40))
        self.dict_img["img_garrow"]  = pygame.transform.smoothscale(self.dict_img["img_garrow"],(40,40))
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

    def load_languages(self):
        """ this function loads all avaliable languages in self.dict_str"""
        if self.options["LANGUAGE"] == "English":
            with open("data/json/eng.json", "r") as read_file:
                self.dict_str=json.load(read_file)
        elif self.options["LANGUAGE"] == "French":
            with open("data/json/fr.json", "r") as read_file:
                self.dict_str=json.load(read_file)

    def create_world(self):
        """
        creates the World object, encapsulating all maps.
        Can be used on the Campaign menu
        """
        self.world = World()

        #creating the map "Kshan"
        mapkshan = Map(self.dict_img["map_kshan"],"map_kshan")
        mp = Level_Sequence(200,200,self.dict_img["img_pointf"],self.dict_img["img_point"])
        mapkshan.set_map_points([mp])

        self.world.set_maps([mapkshan])
        
    def create_characters(self):
        self.characters = []
        with open("data/json/characters.json", "r") as read_file:
            for char in json.load(read_file):
                self.characters.append(Character(char[0],self.dict_img[char[1]],char[2],char[3]))

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

def T(cw,txt,x,y,r=0,g=0,b=0,aliasing=1,size=20,center=True):
    """allows the display of text on screen with or without centering
    the text will be displayed in the window 'cw'
    """
    font = pygame.font.Font(None, size)
    text = font.render(txt, aliasing, (r, g, b))
    if center:
        textpos = text.get_rect(centery=y,centerx=x)
    else:
        textpos = (x,y)
    cw.blit(text, textpos)