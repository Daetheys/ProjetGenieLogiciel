import pygame
from pygame.locals import *
from game.tools.xyinbounds import xyinbounds
from game.tools.text_display import T
from shutil import copy2
import json
from os import listdir
from os import getcwd

from game.level_generation.level_generator import generate_level

#The global variable
BUTTON_LIST = []#to keep an eye on all buttons currently displayed


#Utilitary functions using global variables
def suppress_buttons(n):
    """ suppresses all buttons, except the n first ones """
    global BUTTON_LIST
    for i in range(n,len(BUTTON_LIST)):
        del BUTTON_LIST[n]#si n=2 : titlebanner,exit

"""Reaction functions of the buttons

input   : a game      :
returns : bool x bool :  cnt,quit_all such that:
                        cnt : do we continue the current loop?
                        quit_all : do we quit all loops ?
"""

def no_reaction(g):
    """ the most trivial reaction of a button. It has no effect."""
    return True, False

def reaction_exit(g):#quitte le jeu
    """ exits the game """
    return False,True

def reaction_return(g):#recule d'un rang
    """ the current menu is exited"""
    return False,False

def reaction_changeScreen(resx=1600,resy=900):
    """
    returns a reaction function that changes the resolution into resx,resy
    """
    def f(g):
        g.options["DISPLAYSIZE_X"] = resx
        g.options["DISPLAYSIZE_Y"] = resy
        return True,False
    return f

def reaction_play(text,name):
    """
    allows the player to play a level,
    that will be generated from the music at the file text
    the level will have the name 'name'
    """
    def f(g):
        gl = generate_level(text,name,para=g.options["parallax"])

        g.launch_level(gl,text)
        """ ceci lance le level correspondant """
        g.launch_music(g.menu_music)#relance la musique du menu!

        g.saving()
        return True,False
    return f

def reaction_message(dialkey):
    """
    returns the reaction button displaying the message corresponding to
    the dialogue dialkey when pressed
    """
    def f(g):
        d = g.dict_dial[dialkey]
        d.show(g)
        return True,False
    return f

def reaction_b1(g):
    """
    effect of the upper button of the first menu
    triggers the campaign mode menu
    """
    global BUTTON_LIST
    cnt = True
    cnt_underlying = False
    quit_all = False
    suppress_buttons(2)

    BUTTON_LIST[1].text = "return"
    BUTTON_LIST[1].xmax = 5+25*len(g.dict_str["return"])
    BUTTON_LIST[1].react = reaction_return

    b11 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b11",g.dict_img["img_buttonH"],text="campaign_kshan",react=reaction_b11)
    b12 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b12",g.dict_img["img_buttonH"],g.dict_img["img_buttonD"],text="campaign_fantasy",react=reaction_b12)
    b13 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b13",g.dict_img["img_buttonH"],g.dict_img["img_buttonD"],text="campaign_future")
    if not "Midden Pass" in g.save["accessible"] + g.save["accessed"]:
        b12.activation(False)#désactivé par défaut
    b13.activation(False)#désactivé par défaut

    while cnt:
        cnt,quit_all = g.menu_loop()
        if quit_all:
            cnt = False
            cnt_underlying = False

    BUTTON_LIST[1].text = "exit"
    BUTTON_LIST[1].xmax = 10+25*len(g.dict_str["exit"])
    BUTTON_LIST[1].react = reaction_exit

    suppress_buttons(2)#titlebanner,exit

    return cnt_underlying,quit_all

def reaction_b2(g):
    """
    effect of the second button of the first menu
    triggers the level generator mode menu
    """
    global BUTTON_LIST
    cnt = True
    cnt_underlying = False
    quit_all = False
    suppress_buttons(2)

    BUTTON_LIST[1].text = "return"
    BUTTON_LIST[1].xmax = 5 + 25 * len(g.dict_str["return"])
    BUTTON_LIST[1].react = reaction_return

    b2help = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin,g.b1ymax,g.dict_img["img_buttonD"],"b2help",g.dict_img["img_buttonHD"],text="help",react=reaction_message("dial_help_yourmusicfolder"))

    files = listdir("data/your music")
    files.sort()
    Lf = [b2help]
    for f in files:
        if f.endswith(".wav"):#Remarque : aucune entrée de dictstr ne doit finir par .mp3 !
            b = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*len(Lf),g.b1ymax+g.yoffset*len(Lf),g.dict_img["img_button"],"b pour "+f[:-4],g.dict_img["img_buttonH"],text=f[:-4]+" (wav)",react=reaction_play("data/your music/"+f,f[:-4]))
            Lf.append(b)
        if f.endswith(".mp3"):#Remarque : aucune entrée de dictstr ne doit finir par .mp3 !
            b = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*len(Lf),g.b1ymax+g.yoffset*len(Lf),g.dict_img["img_button"],"b pour "+f[:-4],g.dict_img["img_buttonH"],text=f[:-4]+" (mp3)",react=reaction_play("data/your music/"+f,f[:-4]))
            Lf.append(b)

    #b21 sera activé



    while cnt:
        cnt,quit_all = g.menu_loop(scrolling=True,scrollist=Lf)
        if quit_all:
            cnt = False
            cnt_underlying = False

    BUTTON_LIST[1].text = "exit"
    BUTTON_LIST[1].xmax = 10 + 25 * len(g.dict_str["exit"])
    BUTTON_LIST[1].react = reaction_exit

    suppress_buttons(2)#titlebanner,exit

    return cnt_underlying,quit_all

def reaction_b3(g):
    """
    effect of the lower button of the first menu
    triggers the option menu
    """
    global BUTTON_LIST
    cnt = True
    cnt_underlying = False
    quit_all = False
    suppress_buttons(2)
    BUTTON_LIST[1].text = "return"
    BUTTON_LIST[1].xmax = 5+25*len(g.dict_str["return"])
    BUTTON_LIST[1].react = reaction_return

    b31 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b31",g.dict_img["img_buttonH"],text="volume")
    b32 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b32",g.dict_img["img_buttonH"],text="choose_language",react=reaction_b32)
    b33 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b33",g.dict_img["img_buttonH"],text="reset_save",react=reaction_b33)
    b34 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b34",g.dict_img["img_buttonH"],text="graphics",react=reaction_b34)
    b35 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b35",g.dict_img["img_buttonH"],text="credits")
    b36 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b36",g.dict_img["img_buttonH"],text="achievements")

    while cnt:
        cnt,quit_all = g.menu_loop()
        if quit_all:
            cnt = False
            cnt_underlying = False

    with open("data/json/options.json","w") as f:
        f.write(json.dumps(g.options))

    BUTTON_LIST[1].text = "exit"
    BUTTON_LIST[1].xmax = 10+25*len(g.dict_str["exit"])
    BUTTON_LIST[1].react = reaction_exit

    suppress_buttons(2)

    return cnt_underlying,quit_all

def reaction_b11(g):
    """
    effect of the first button campaign mode menu
    triggers the map "Kshan"
     """
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)

    bg =  pygame.transform.smoothscale(g.world.get_map("map_kshan").image, (g.options["DISPLAYSIZE_X"],g.options["DISPLAYSIZE_Y"]))


    while cnt:
        cnt,quit_all = g.map_loop(bg=bg,map=g.world.get_map("map_kshan"))
        if quit_all:
            cnt = False
            cnt_underlying = False

    b11 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b11",g.dict_img["img_buttonH"],text="campaign_kshan",react=reaction_b11)
    b12 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b12",g.dict_img["img_buttonH"],g.dict_img["img_buttonD"],text="campaign_fantasy",react=reaction_b12)
    b13 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b13",g.dict_img["img_buttonH"],g.dict_img["img_buttonD"],text="campaign_future")
    if not "Midden Pass" in g.save["accessible"] + g.save["accessed"]:
        b12.activation(False)#désactivé par défaut
    b13.activation(False)#désactivé par défaut

    return cnt_underlying,quit_all

def reaction_b12(g):
    """
    effect of the first button campaign mode menu
    triggers the map "Fantasy"
     """
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)

    bg =  pygame.transform.smoothscale(g.world.get_map("map_fantasy").image, (g.options["DISPLAYSIZE_X"],g.options["DISPLAYSIZE_Y"]))


    while cnt:
        cnt,quit_all = g.map_loop(bg=bg,map=g.world.get_map("map_fantasy"))
        if quit_all:
            cnt = False
            cnt_underlying = False

    suppress_buttons(2)#titlebanner,exit

    b11 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b11",g.dict_img["img_buttonH"],text="campaign_kshan",react=reaction_b11)
    b12 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b12",g.dict_img["img_buttonH"],g.dict_img["img_buttonD"],text="campaign_fantasy",react=reaction_b12)
    b13 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b13",g.dict_img["img_buttonH"],g.dict_img["img_buttonD"],text="campaign_future")
    if not "Midden Pass" in g.save["accessible"] + g.save["accessed"]:
        b12.activation(False)#désactivé par défaut
    b13.activation(False)#désactivé par défaut

    return cnt_underlying,quit_all

def reaction_b32(g):
    """language choice menu reaction button"""
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)


    b321 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b321",g.dict_img["img_buttonH"],text="English",react=reaction_b321)
    b322 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b322",g.dict_img["img_buttonH"],text="Français",react=reaction_b322)
    b323 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b323",g.dict_img["img_buttonH"],text="Español")
    b324 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*3,g.b1ymax+g.yoffset*3,g.dict_img["img_button"],"b324",g.dict_img["img_buttonH"],text="Esperanto")
    b325 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*4,g.b1ymax+g.yoffset*4,g.dict_img["img_button"],"b325",g.dict_img["img_buttonH"],text="Русский язык")
    b326 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*5,g.b1ymax+g.yoffset*5,g.dict_img["img_button"],"b326",g.dict_img["img_buttonH"],text="日本語")
    b323.activation(False)
    b324.activation(False)
    b325.activation(False)
    b326.activation(False)

    while cnt:
        cnt,quit_all = g.menu_loop(scrolling=True,scrollist=[b321,b322,b323,b324,b325,b326])
        if quit_all:
            cnt = False
            cnt_underlying = False

    suppress_buttons(2)
    b31 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b31",g.dict_img["img_buttonH"],text="volume")
    b32 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b32",g.dict_img["img_buttonH"],text="choose_language",react=reaction_b32)
    b33 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b33",g.dict_img["img_buttonH"],text="reset_save",react=reaction_b33)
    b34 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b34",g.dict_img["img_buttonH"],text="graphics",react=reaction_b34)
    b35 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b35",g.dict_img["img_buttonH"],text="credits")
    b36 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b36",g.dict_img["img_buttonH"],text="achievements")

    return cnt_underlying,quit_all



def reaction_b34(g):
    """graphics choice menu reaction button"""
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)


    b341 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b341",g.dict_img["img_buttonH"],text="Activate Fullscreen",react=reaction_b341)
    b342 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b342",g.dict_img["img_buttonH"],text="1600x900",react=reaction_changeScreen(resx=1600,resy=900))
    b343 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b343",g.dict_img["img_buttonH"],text="1280x720",react=reaction_changeScreen(resx=1280,resy=720))
    b344 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*3,g.b1ymax+g.yoffset*3,g.dict_img["img_button"],"b344",g.dict_img["img_buttonH"],text="1366x768",react=reaction_changeScreen(resx=1366,resy=768))
    b345 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*4,g.b1ymax+g.yoffset*4,g.dict_img["img_button"],"b345",g.dict_img["img_buttonH"],text="1920x1080",react=reaction_changeScreen(resx=1920,resy=1080))
    b346 = ButtonMenu(g,g.b1xmin,g.b1xmax,g.b1ymin+g.yoffset*5,g.b1ymax+g.yoffset*5,g.dict_img["img_button"],"b346",g.dict_img["img_buttonH"],text="2560x1440",react=reaction_changeScreen(resx=2560,resy=1440))

    if g.options["modeECRAN"]:#if is in FULLSCREEN
        b341.text = "Disable Fullscreen"
    else:
        b341.text = "Activate Fullscreen"
    while cnt:
        cnt,quit_all = g.menu_loop(scrolling=True,scrollist=[b341,b342,b343,b344,b345,b346])
        if g.options["modeECRAN"]:#if is in FULLSCREEN
            b341.text = "Disable Fullscreen"
        else:
            b341.text = "Activate Fullscreen"
        if quit_all:
            cnt = False
            cnt_underlying = False

    suppress_buttons(2)
    b31 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b31",g.dict_img["img_buttonH"],text="volume")
    b32 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b32",g.dict_img["img_buttonH"],text="choose_language",react=reaction_b32)
    b33 = ButtonMenu(g,g.b31xmin,g.b31xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b33",g.dict_img["img_buttonH"],text="reset_save",react=reaction_b33)
    b34 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin,g.b1ymax,g.dict_img["img_button"],"b34",g.dict_img["img_buttonH"],text="graphics",react=reaction_b34)
    b35 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin+g.yoffset,g.b1ymax+g.yoffset,g.dict_img["img_button"],"b35",g.dict_img["img_buttonH"],text="credits")
    b36 = ButtonMenu(g,g.b32xmin,g.b32xmax,g.b1ymin+g.yoffset*2,g.b1ymax+g.yoffset*2,g.dict_img["img_button"],"b36",g.dict_img["img_buttonH"],text="achievements")

    return cnt_underlying,quit_all

def reaction_b341(g):
    """ Toggle Fullscreen"""
    g.options["modeECRAN"] = FULLSCREEN - g.options["modeECRAN"]
    return True,False

def reaction_b321(g):
    g.options["LANGUAGE"] = "English"
    g.load_languages()
    for b in BUTTON_LIST:
        if b.name == "exit":
            b.text = g.dict_str["return"]
            b.xmax = 5 + 25*len(g.dict_str["return"])
    return True, False

def reaction_b322(g):
    g.options["LANGUAGE"] = "French"
    g.load_languages()
    for b in BUTTON_LIST:
        if b.name == "exit":
            b.text = g.dict_str["return"]
            b.xmax = 5 + 25*len(g.dict_str["return"])
    return True, False

def reaction_b33(g):
    """ reaction of the erase savefile button """
    d = g.dict_dial["dial_erase_savefile"]
    if d.show(g):#est ce que Echap/la croix a été pressée?
        return True,False
    try:
        with open("data/json/default_options.json","r") as file:
            g.options = json.load(file)
        copy2("data/json/default_options.json","data/json/options.json")
    except FileNotFoundError:
        print("File Not Found.")
    g.load_languages()
    for b in BUTTON_LIST:
        if b.name == "exit":
            b.text = "return"
            b.xmax = 5 + 25*len(g.dict_str["return"])
    return True,False

class ButtonMenu:

    def __init__(self,g,xm,xM,ym,yM,img,name="Unnamed",picH=None,picD=None,text=None,react=no_reaction,add_to_list=True):
        self.g = g#the game where the buttons will be displayed
        assert g.yoffset is not None
        self.xmin = xm
        self.xmax = xM
        self.ymin = ym
        self.ymax = yM
        self.pic = img
        self.activated = True
        if picH is None:self.picH = img
        else: self.picH = picH#hovering
        if picD is None: self.picD = img
        else: self.picD = picD#deactivated
        if text is None: self.text = ""
        else: self.text = text#displayed text
        self.t = 0
        self.up = True
        if add_to_list:
            BUTTON_LIST.append(self)#to keep an eye on all buttons
        self.name = name
        self.speed = 1
        self.period = 1
        self.react = react
        self.visible = True
        self.was_active = True#manages activation ~ disappearance relations
        self.offsetX = 0

    def __repr__(self):
        return self.name + '= Button(%s<x<%s, %s<y<%s)\n' % (self.xmin, self.xmax, self.ymin, self.ymax)

    def __displayedY(self,yy):
        return yy - self.period//2 + ((self.t//self.speed)%self.period)

    def set_offset(self,offset):
        """ sets the offset of the text """
        self.offsetX = offset

    def boundaries(self):
        """ returns the visible boundaries of self"""
        return self.xmin,self.xmax,self.__displayedY(self.ymin),self.__displayedY(self.ymax)

    def activation(self,flag):
        self.activated = flag
        self.was_active = flag
        return self

    def appear(self):
        """ an invisible button appears"""
        self.visible = True
        self.activated = self.was_active
    def disappear(self):
        """ a button disappears """
        self.visible = False
        self.was_active = self.activated
        self.activated = False

    def display(self,period=None,speed=None,refresh=False,lock=True):
        """allow for the display of buttons"""
        if self.visible:
            mx,my = pygame.mouse.get_pos()
            if self.activated:
                if xyinbounds(mx,my,self):
                    picture = self.picH
                else:
                    picture = self.pic
            else:
                picture = self.picD
            if speed is None: speed = self.speed
            else: self.speed = speed
            if period is None: period = self.period
            else: self.period = period
            if period <= 1: self.g.win().blit(picture,(self.xmin-self.offsetX,self.ymin))
            else:
                if self.up:self.t += 1
                else: self.t -= 1
                if self.t >= period - 1:
                    self.up = False
                elif self.t <= 0:
                    self.up = True
                self.g.win().blit(picture,(self.xmin-self.offsetX,self.__displayedY(self.ymin)))
            if self.activated:
                T(self.g.win(),self.g.dict_str_dflt(self.text),(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,size=50)
            else:
                T(self.g.win(),self.g.dict_str_dflt(self.text),(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,50,50,50,size=50)
                if lock: self.g.win().blit(self.g.dict_img["img_layer_lock"],(self.xmin-self.offsetX,self.__displayedY(self.ymin)))
            if refresh: g.flip()
