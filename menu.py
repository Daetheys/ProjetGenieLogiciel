"""
Menu v8
"""

import sys
import pygame
import json
pygame.init()
from pygame.locals import *
pygame.mixer.init()
from tools import *

#Display
FRAMEPERSECONDLIMIT = 30
modeECRAN = FULLSCREEN  #modeECRAN = 0 ou FULLSCREEN
DISPLAYSIZE_X = 1600
DISPLAYSIZE_Y = 900
fenetre = pygame.display.set_mode((DISPLAYSIZE_X, DISPLAYSIZE_Y),modeECRAN)#1920*1080
pygame.display.set_icon(pygame.image.load("_/img/icon.ico"))


def T(txt,x,y,r=0,g=0,b=0,aliasing=1,size=20,center=True):
    """allows the display of text on screen with or without centering"""
    font = pygame.font.Font(None, size)
    text = font.render(txt, aliasing, (r, g, b))
    if center:
        textpos = text.get_rect(centery=y,centerx=x)
    else:
        textpos = (x,y)
    fenetre.blit(text, textpos)


#Images
with open("_/json/img.json", "r") as read_file:
    dict_img=json.load(read_file,object_hook=create_img)

#Title
pygame.display.set_caption("CAN·A·BAELDE")
fenetre.blit(dict_img["img_background"],(0,0))
pygame.display.flip()

#Music
""" menu music is  disabled """
#pygame.mixer.music.load(music_menu)
#pygame.mixer.music.fadeout(500)
#pygame.mixer.music.play(-1)

#Other constants
LANGUAGE = "French"
BUTTON_LIST = []#to keep an eye on all buttons currently displayed


if LANGUAGE == "English":
    with open("_/json/eng.json", "r") as read_file:
        dict_str=json.load(read_file)
elif LANGUAGE == "French":
    with open("_/json/fr.json", "r") as read_file:
        dict_str=json.load(read_file)
    
class buttonMenu:

    def __init__(self,xm,xM,ym,yM,img=dict_img["img_default"],name="Unnamed",picH=None,picD=None,text=None,react=no_reaction):
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
        BUTTON_LIST.append(self)#to keep an eye on all buttons
        self.name = name
        self.speed = 1
        self.period = 1
        self.react = react
    def __repr__(self):
        return self.name + '= Button(%s<x<%s, %s<y<%s)\n' % (self.xmin, self.xmax, self.ymin, self.ymax)
    
    def __displayedY(self,yy):
        return yy - self.period//2 + ((self.t//self.speed)%self.period)
         
    def boundaries(self):
        """ returns the visible boundaries of self"""
        return self.xmin,self.xmax,self.__displayedY(self.ymin),self.__displayedY(self.ymax)
    
    def activation(self,flag):self.activated=flag
    
    def display(self,period=None,speed=None,refresh=False):
        """allow for the display of buttons"""
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
        if period <= 1: fenetre.blit(picture,(self.xmin,self.ymin))
        else:
            if self.up:self.t += 1
            else: self.t -= 1
            if self.t >= period - 1:
                self.up = False
            elif self.t <= 0:
                self.up = True
            fenetre.blit(picture,(self.xmin,self.__displayedY(self.ymin)))
        if self.activated:
            T(self.text,(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,size=50)
        else:
            T(self.text,(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,50,50,50,size=50)
            fenetre.blit(dict_img["img_layer_lock"],(self.xmin,self.__displayedY(self.ymin)))
        if refresh: pygame.display.flip()
    
#Reaction functions of the buttons
def suppress_buttons(n):
    """ suppresses all buttons, except the n first ones """
    global BUTTON_LIST
    for i in range(n,len(BUTTON_LIST)):
        del BUTTON_LIST[n]#si n=2 : titlebanner,exit

def reaction_b1():
    """ 
    effect of the upper button of the first menu
    triggers the campaign mode menu
    """
    global BUTTON_LIST
    cnt = True
    cnt_underlying = False
    quit_all = False
    suppress_buttons(2)
    
    BUTTON_LIST[1].text = dict_str["return"]
    BUTTON_LIST[1].xmax = 5+25*len(dict_str["return"])
    BUTTON_LIST[1].react = reaction_return

    b11 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,dict_img["img_button"],"b11",dict_img["img_buttonH"],text=dict_str["campaign_kshan"],react=reaction_b11)
    b12 = buttonMenu(b1xmin,b1xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b12",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_fantasy"]).activation(False)#désactivé par défaut
    b13 = buttonMenu(b1xmin,b1xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b13",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_future"]).activation(False)#désactivé par défaut

    while cnt:
        cnt,quit_all = menu_loop()
        if quit_all:
            cnt = False
            cnt_underlying = False
            
    BUTTON_LIST[1].text = dict_str["exit"]
    BUTTON_LIST[1].xmax = 10+25*len(dict_str["exit"])
    BUTTON_LIST[1].react = reaction_exit
    
    suppress_buttons(2)#titlebanner,exit
        
    return cnt_underlying,quit_all
  
def reaction_b3():
    """ 
    effect of the lower button of the first menu
    triggers the option menu
    """
    
    global BUTTON_LIST
    cnt = True
    cnt_underlying = False
    quit_all = False
    suppress_buttons(2)
    BUTTON_LIST[1].text = dict_str["return"]
    BUTTON_LIST[1].xmax = 5+25*len(dict_str["return"])
    BUTTON_LIST[1].react = reaction_return

    b31 = buttonMenu(b31xmin,b31xmax,b1ymin,b1ymax,dict_img["img_button"],"b31",dict_img["img_buttonH"],text=dict_str["volume"])
    b32 = buttonMenu(b31xmin,b31xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b32",dict_img["img_buttonH"],text=dict_str["choose_language"],react=reaction_b32)
    b33 = buttonMenu(b31xmin,b31xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b33",dict_img["img_buttonH"],text=dict_str["reset_save"])
    b34 = buttonMenu(b32xmin,b32xmax,b1ymin,b1ymax,dict_img["img_button"],"b34",dict_img["img_buttonH"],text=dict_str["graphics"])
    b35 = buttonMenu(b32xmin,b32xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b35",dict_img["img_buttonH"],text=dict_str["credits"])
    b36 = buttonMenu(b32xmin,b32xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b36",dict_img["img_buttonH"],text=dict_str["achievements"])

    while cnt:
        cnt,quit_all = menu_loop()
        if quit_all:
            cnt = False
            cnt_underlying = False
            
    BUTTON_LIST[1].text = dict_str["exit"]
    BUTTON_LIST[1].xmax = 10+25*len(dict_str["exit"])
    BUTTON_LIST[1].react = reaction_exit

    suppress_buttons(2)
    
    return cnt_underlying,quit_all

def reaction_exit():#quitte le jeu
    return False,True  
        
def reaction_return():#recule d'un rang
    return False,False

def reaction_b11():
    """
    effect of the first button campaign mode menu
    triggers the map "Kshan"
     """
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)
    #TODO buttons on the map
    
    #b111 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,dict_img["img_button"],"b111",dict_img["img_buttonH"],text="")
    while cnt:
        cnt,quit_all = menu_loop(background = dict_img["map_kshan"])
        if quit_all:
            cnt = False
            cnt_underlying = False
    
    #suppress_buttons(2)#titlebanner,exit

    b11 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,dict_img["img_button"],"b11",dict_img["img_buttonH"],text=dict_str["campaign_kshan"],react=reaction_b11)
    b12 = buttonMenu(b1xmin,b1xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b12",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_fantasy"]).activation(False)#désactivé par défaut
    b13 = buttonMenu(b1xmin,b1xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b13",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_future"]).activation(False)#désactivé par défaut

    return cnt_underlying,quit_all
    
def reaction_b32():
    """language"""
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)

    b321 = buttonMenu(b31xmin,b31xmax,b1ymin,b1ymax,dict_img["img_button"],"b321",dict_img["img_buttonH"],text="English")
    b322 = buttonMenu(b31xmin,b31xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b322",dict_img["img_buttonH"],text="Français")
    b323 = buttonMenu(b31xmin,b31xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b323",dict_img["img_buttonH"],text="Español")
    b324 = buttonMenu(b32xmin,b32xmax,b1ymin,b1ymax,dict_img["img_button"],"b324",dict_img["img_buttonH"],text="Esperanto")
    b325 = buttonMenu(b32xmin,b32xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b325",dict_img["img_buttonH"],text="Русский язык")
    b326 = buttonMenu(b32xmin,b32xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b326",dict_img["img_buttonH"],text="日本語")
    

    while cnt:
        cnt,quit_all = menu_loop()
        if quit_all:
            cnt = False
            cnt_underlying = False

    suppress_buttons(2)
    b31 = buttonMenu(b31xmin,b31xmax,b1ymin,b1ymax,dict_img["img_button"],"b31",dict_img["img_buttonH"],text=dict_str["volume"])
    b32 = buttonMenu(b31xmin,b31xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b32",dict_img["img_buttonH"],text=dict_str["choose_language"],react=reaction_b32)
    b33 = buttonMenu(b31xmin,b31xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b33",dict_img["img_buttonH"],text=dict_str["reset_save"])
    b34 = buttonMenu(b32xmin,b32xmax,b1ymin,b1ymax,dict_img["img_button"],"b34",dict_img["img_buttonH"],text=dict_str["graphics"])
    b35 = buttonMenu(b32xmin,b32xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b35",dict_img["img_buttonH"],text=dict_str["credits"])
    b36 = buttonMenu(b32xmin,b32xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b36",dict_img["img_buttonH"],text=dict_str["achievements"])
    
    return cnt_underlying,quit_all
    
def menu_loop(cnt = True,quit_all=False,background = None):
    """
    function used for various loops. returns:
      continue (whether the loop nesting it stops)
      quit_all (whether the full game stops)
    """
    if background == None:
        background = dict_img["img_background"]
    global BUTTON_LIST
    pygame.time.Clock().tick(FRAMEPERSECONDLIMIT)
    
    #BACKGROUND DISPLAY
    fenetre.blit(background,(0,0))
    
    #BUTTON DISPLAY
    for b in BUTTON_LIST:
        if b.name == "banner":
            b.display(5,3)
        elif b.name == "exit":
            b.display(1,1)
        else:
            b.display(20)
    pygame.display.flip()
    
    #KEYBOARD HANDLER
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit_all = True
                cnt = False
            if event.key == K_p:
                pygame.mixer.music.pause()
        #MOUSE EVENTS HANDLER
        if event.type == MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos() 
            for b in BUTTON_LIST:
                if xyinbounds(mx,my,b):
                    print(b.name)
                    cntb,quit_allb = b.react()
                    cnt  = cnt and cntb
                    quit_all = quit_all or quit_allb
    
    return cnt,quit_all

#Basic buttons
titlebanner = buttonMenu(105,1456,25,173,dict_img["img_titlebanner"],"banner")
exit = buttonMenu(10,5+20*len(dict_str["exit"]),DISPLAYSIZE_Y-50,DISPLAYSIZE_Y,dict_img["img_void"],"exit",text=dict_str["exit"],react=reaction_exit)

quitter_jeu = False
continuer_menu =  True
continuer_menu_campagne = False
continuer_map  =  False
while not quitter_jeu:
    b1xmin = 550
    b1xmax = 1050
    b1ymin = 230
    b1ymax = 400
    b31xmin = DISPLAYSIZE_X/3-250
    b31xmax = DISPLAYSIZE_X/3+250
    b32xmin = 2*DISPLAYSIZE_X/3-250
    b32xmax = 2*DISPLAYSIZE_X/3+250
    b1 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,dict_img["img_button"],"b1",dict_img["img_buttonH"],text=dict_str["campaign_mode"],react=reaction_b1)
    b2 = buttonMenu(b1xmin,b1xmax,b1ymin+200,b1ymax+200,dict_img["img_button"],"b2",dict_img["img_button"],dict_img["img_buttonD"],text=dict_str["free_play"]).activation(False)#désactivé par défaut
    b3 = buttonMenu(b1xmin,b1xmax,b1ymin+400,b1ymax+400,dict_img["img_button"],"b3",dict_img["img_buttonH"],text=dict_str["options"],react=reaction_b3)

    while continuer_menu:
        continuer_menu,quitter_jeu = menu_loop()
        if quitter_jeu:
            continuer_menu = False
    continuer_menu = True
pygame.display.quit()
pygame.quit()
#sys.exit(0)