"""
Menu v0.8.6
-banner is centered
-buttons are in the middle of the screen for all screen sizes
"""

import sys
import pygame
import json
from pygame.locals import *
from tools import *


if __name__ == '__main__':
    #Display
    with open("data/json/options.json","r") as file:
        OPTIONS = json.load(file)
        #OPTIONS["modeECRAN"]  = 0 ou FULLSCREEN
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("CAN·A·BAELDE")
    pygame.display.set_icon(pygame.image.load("data/img/icon.ico"))
    fenetre = pygame.display.set_mode((OPTIONS["DISPLAYSIZE_X"], OPTIONS["DISPLAYSIZE_Y"]),OPTIONS["modeECRAN"])#1920*1080

    fenetre.blit(pygame.image.load("data/img/blvr.png"),(0,0))
    pygame.display.flip()

    #Images
    with open("data/json/img.json", "r") as read_file:
        dict_img=json.load(read_file,object_hook=create_img)
    dict_img["img_arrow"]  = pygame.transform.smoothscale(dict_img["img_arrow"],(40,40))
    dict_img["img_garrow"]  = pygame.transform.smoothscale(dict_img["img_garrow"],(40,40))

    #Other constants
    BUTTON_LIST = []#to keep an eye on all buttons currently displayed

    quitter_jeu = False
    continuer_menu =  True
    b1xmin = OPTIONS["DISPLAYSIZE_X"]//2 - 250
    b1xmax = OPTIONS["DISPLAYSIZE_X"]//2 + 250
    b1ymin = 230
    b1ymax = 400
    b31xmin = OPTIONS["DISPLAYSIZE_X"]//3-250
    b31xmax = OPTIONS["DISPLAYSIZE_X"]//3+250
    b32xmin = 2*OPTIONS["DISPLAYSIZE_X"]//3-250
    b32xmax = 2*OPTIONS["DISPLAYSIZE_X"]//3+250
    yoffset = int(OPTIONS["DISPLAYSIZE_Y"]/4.5)

    if OPTIONS["LANGUAGE"] == "English":
        with open("data/json/eng.json", "r") as read_file:
            dict_str=json.load(read_file)
    elif OPTIONS["LANGUAGE"] == "French":
        with open("data/json/fr.json", "r") as read_file:
            dict_str=json.load(read_file)

    #Utilitary functions using global variables
    def suppress_buttons(n):
        """ suppresses all buttons, except the n first ones """
        global BUTTON_LIST
        for i in range(n,len(BUTTON_LIST)):
            del BUTTON_LIST[n]#si n=2 : titlebanner,exit

    def T(txt,x,y,r=0,g=0,b=0,aliasing=1,size=20,center=True):
        """allows the display of text on screen with or without centering"""
        font = pygame.font.Font(None, size)
        text = font.render(txt, aliasing, (r, g, b))
        if center:
            textpos = text.get_rect(centery=y,centerx=x)
        else:
            textpos = (x,y)
        fenetre.blit(text, textpos)
    #Music
    """ menu music is  disabled """
    #pygame.mixer.music.load(music_menu)
    #pygame.mixer.music.fadeout(500)
    #pygame.mixer.music.play(-1)

class buttonMenu:

    def __init__(self,xm,xM,ym,yM,img=dict_img["img_default"],name="Unnamed",picH=None,picD=None,text=None,react=no_reaction,add_to_list=True):
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
    def __repr__(self):
        return self.name + '= Button(%s<x<%s, %s<y<%s)\n' % (self.xmin, self.xmax, self.ymin, self.ymax)
    
    def __displayedY(self,yy):
        return yy - self.period//2 + ((self.t//self.speed)%self.period)
         
    def boundaries(self):
        """ returns the visible boundaries of self"""
        return self.xmin,self.xmax,self.__displayedY(self.ymin),self.__displayedY(self.ymax)
    
    def activation(self,flag):
        self.activated = flag
        self.was_active = flag
    def appear(self):
        """ an invisible button appears"""
        self.visible = True
        self.activated = self.was_active
    def disappear(self):
        """ a button disappears """
        self.visible = False
        self.was_active = self.activated
        self.activated = False
    def display(self,period=None,speed=None,refresh=False):
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

def reaction_exit():#quitte le jeu
    """ exits the game """
    return False,True

def reaction_return():#recule d'un rang
    """ the current menu is exited"""
    return False,False

def reaction_changeScreen(resx=1600,resy=900):
    """
    returns a functions that changes the resolution into resx,resy """
    def f():
        global OPTIONS,OPTIONS
        OPTIONS["DISPLAYSIZE_X"] = resx
        OPTIONS["DISPLAYSIZE_Y"] = resy
        return True,False
    return f

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
    b12 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b12",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_fantasy"])
    b13 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b13",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_future"])
    b12.activation(False)#désactivé par défaut
    b13.activation(False)#désactivé par défaut

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
    global BUTTON_LIST,OPTIONS
    cnt = True
    cnt_underlying = False
    quit_all = False
    suppress_buttons(2)
    BUTTON_LIST[1].text = dict_str["return"]
    BUTTON_LIST[1].xmax = 5+25*len(dict_str["return"])
    BUTTON_LIST[1].react = reaction_return

    b31 = buttonMenu(b31xmin,b31xmax,b1ymin,b1ymax,dict_img["img_button"],"b31",dict_img["img_buttonH"],text=dict_str["volume"])
    b32 = buttonMenu(b31xmin,b31xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b32",dict_img["img_buttonH"],text=dict_str["choose_language"],react=reaction_b32)
    b33 = buttonMenu(b31xmin,b31xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b33",dict_img["img_buttonH"],text=dict_str["reset_save"])
    b34 = buttonMenu(b32xmin,b32xmax,b1ymin,b1ymax,dict_img["img_button"],"b34",dict_img["img_buttonH"],text=dict_str["graphics"],react=reaction_b34)
    b35 = buttonMenu(b32xmin,b32xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b35",dict_img["img_buttonH"],text=dict_str["credits"])
    b36 = buttonMenu(b32xmin,b32xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b36",dict_img["img_buttonH"],text=dict_str["achievements"])

    while cnt:
        cnt,quit_all = menu_loop()
        if quit_all:
            cnt = False
            cnt_underlying = False

    with open("data/json/options.json","w") as f:
        f.write(json.dumps(OPTIONS))

    BUTTON_LIST[1].text = dict_str["exit"]
    BUTTON_LIST[1].xmax = 10+25*len(dict_str["exit"])
    BUTTON_LIST[1].react = reaction_exit

    suppress_buttons(2)
    
    return cnt_underlying,quit_all

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
    b12 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b12",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_fantasy"])
    b13 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b13",dict_img["img_buttonH"],dict_img["img_buttonD"],text=dict_str["campaign_future"])
    b12.activation(False)#désactivé par défaut
    b13.activation(False)#désactivé par défaut

    return cnt_underlying,quit_all


def reaction_b32():
    """language choice menu reaction button"""
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)

    
    b321 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,dict_img["img_button"],"b321",dict_img["img_buttonH"],text="English",react=reaction_b321)
    b322 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b322",dict_img["img_buttonH"],text="Français",react=reaction_b322)
    b323 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b323",dict_img["img_buttonH"],text="Español")
    b324 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*3,b1ymax+yoffset*3,dict_img["img_button"],"b324",dict_img["img_buttonH"],text="Esperanto")
    b325 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*4,b1ymax+yoffset*4,dict_img["img_button"],"b325",dict_img["img_buttonH"],text="Русский язык")
    b326 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*5,b1ymax+yoffset*5,dict_img["img_button"],"b326",dict_img["img_buttonH"],text="日本語")
    b323.activation(False)
    b324.activation(False)
    b325.activation(False)
    b326.activation(False)

    while cnt:
        cnt,quit_all = menu_loop(scrolling=True,scrollist=[b321,b322,b323,b324,b325,b326])
        if quit_all:
            cnt = False
            cnt_underlying = False

    suppress_buttons(2)
    b31 = buttonMenu(b31xmin,b31xmax,b1ymin,b1ymax,dict_img["img_button"],"b31",dict_img["img_buttonH"],text=dict_str["volume"])
    b32 = buttonMenu(b31xmin,b31xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b32",dict_img["img_buttonH"],text=dict_str["choose_language"],react=reaction_b32)
    b33 = buttonMenu(b31xmin,b31xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b33",dict_img["img_buttonH"],text=dict_str["reset_save"])
    b34 = buttonMenu(b32xmin,b32xmax,b1ymin,b1ymax,dict_img["img_button"],"b34",dict_img["img_buttonH"],text=dict_str["graphics"],react=reaction_b34)
    b35 = buttonMenu(b32xmin,b32xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b35",dict_img["img_buttonH"],text=dict_str["credits"])
    b36 = buttonMenu(b32xmin,b32xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b36",dict_img["img_buttonH"],text=dict_str["achievements"])
    
    return cnt_underlying,quit_all



def reaction_b34():
    """graphics choice menu reaction button"""
    global BUTTON_LIST
    cnt = True
    cnt_underlying = True
    quit_all = False
    suppress_buttons(2)

    
    b341 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,dict_img["img_button"],"b341",dict_img["img_buttonH"],text=dict_str["Activate Fullscreen"],react=reaction_b341)
    b342 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b342",dict_img["img_buttonH"],text="1600x900",react=reaction_changeScreen(resx=1600,resy=900))
    b343 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b343",dict_img["img_buttonH"],text="1280x720",react=reaction_changeScreen(resx=1280,resy=720))
    b344 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*3,b1ymax+yoffset*3,dict_img["img_button"],"b344",dict_img["img_buttonH"],text="1366x768",react=reaction_changeScreen(resx=1366,resy=768))
    b345 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*4,b1ymax+yoffset*4,dict_img["img_button"],"b345",dict_img["img_buttonH"],text="1920x1080",react=reaction_changeScreen(resx=1920,resy=1080))
    b346 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*5,b1ymax+yoffset*5,dict_img["img_button"],"b346",dict_img["img_buttonH"],text="2560x1440",react=reaction_changeScreen(resx=2560,resy=1440))
    #b344.activation(False)
    #b343.activation(False)
    #b345.activation(False)
    #b346.activation(False)
    if OPTIONS["modeECRAN"]:#if is in FULLSCREEN
        b341.text = dict_str["Disable Fullscreen"]
    else:
        b341.text = dict_str["Activate Fullscreen"]
    while cnt:
        cnt,quit_all = menu_loop(scrolling=True,scrollist=[b341,b342,b343,b344,b345,b346])
        if OPTIONS["modeECRAN"]:#if is in FULLSCREEN
            b341.text = dict_str["Disable Fullscreen"]
        else:
            b341.text = dict_str["Activate Fullscreen"]
        if quit_all:
            cnt = False
            cnt_underlying = False

    suppress_buttons(2)
    b31 = buttonMenu(b31xmin,b31xmax,b1ymin,b1ymax,dict_img["img_button"],"b31",dict_img["img_buttonH"],text=dict_str["volume"])
    b32 = buttonMenu(b31xmin,b31xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b32",dict_img["img_buttonH"],text=dict_str["choose_language"],react=reaction_b32)
    b33 = buttonMenu(b31xmin,b31xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b33",dict_img["img_buttonH"],text=dict_str["reset_save"])
    b34 = buttonMenu(b32xmin,b32xmax,b1ymin,b1ymax,dict_img["img_button"],"b34",dict_img["img_buttonH"],text=dict_str["graphics"],react=reaction_b34)
    b35 = buttonMenu(b32xmin,b32xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b35",dict_img["img_buttonH"],text=dict_str["credits"])
    b36 = buttonMenu(b32xmin,b32xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b36",dict_img["img_buttonH"],text=dict_str["achievements"])

    return cnt_underlying,quit_all

def reaction_b341():
    """ Toggle Fullscreen"""
    global OPTIONS
    OPTIONS["modeECRAN"] = FULLSCREEN - OPTIONS["modeECRAN"]
    return True,False

def reaction_b321():
    global dict_str,OPTIONS
    OPTIONS["LANGUAGE"] = "English"
    with open("data/json/eng.json", "r") as read_file:
        dict_str = json.load(read_file)
    for b in BUTTON_LIST:
        if b.name == "exit":
            b.text = dict_str["return"]
            b.xmax = 5 + 25*len(dict_str["return"])
    return True, False
        
def reaction_b322():
    global dict_str,OPTIONS
    OPTIONS["LANGUAGE"] = "French"
    with open("data/json/fr.json", "r") as read_file:
        dict_str = json.load(read_file)
    for b in BUTTON_LIST:
        if b.name == "exit":
            b.text = dict_str["return"]
            b.xmax = 5 + 25*len(dict_str["return"])
    return True, False

def menu_loop(cnt = True,quit_all=False,background = None,scrolling=False,scrollist=[]):
    """
    function used for various loops. returns:
      continue (whether the loop nesting it stops)
      quit_all (whether the full game stops)
    """
    if background == None:
        background = dict_img["img_background"]
    global BUTTON_LIST
    pygame.time.Clock().tick(OPTIONS["FPS"])
    
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
    if scrolling and len(scrollist):
        if scrollist[-1].ymax > b1ymax+400:
            fenetre.blit(dict_img["img_arrow"],(OPTIONS["DISPLAYSIZE_X"]//2+250,300))
        else:
            fenetre.blit(dict_img["img_garrow"],(OPTIONS["DISPLAYSIZE_X"]//2+250,300))
        if scrollist[0].ymin < b1ymin:
            fenetre.blit(pygame.transform.flip(dict_img["img_arrow"],False,True),(OPTIONS["DISPLAYSIZE_X"]//2+250,250))
        else:
            fenetre.blit(pygame.transform.flip(dict_img["img_garrow"],False,True),(OPTIONS["DISPLAYSIZE_X"]//2+250,250))
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
            if event.button == 1:
                for b in BUTTON_LIST:
                    if xyinbounds(mx,my,b):
                        print(b.name)
                        cntb,quit_allb = b.react()
                        cnt  = cnt and cntb
                        quit_all = quit_all or quit_allb

            if scrolling and len(scrollist):
                if event.button == 5:
                    if scrollist[-1].ymax > b1ymax+400:
                        #empeche d'aller trop loin en bas
                        #print("scroll up")
                        for b in scrollist:
                            b.ymin -= yoffset
                            b.ymax -= yoffset
                            if b.ymin < b1ymin:
                                if b.visible:
                                    b.disappear()
                            elif b.ymax <= b1ymax+400:
                                b.appear()
                elif event.button == 4:
                    if scrollist[0].ymin < b1ymin:
                        #empeche d'aller trop loin en haut
                        #print("scroll down")
                        for b in scrollist:
                            b.ymin += yoffset
                            b.ymax += yoffset
                            if b.ymax > b1ymax+400:
                                if b.visible:
                                    b.disappear()
                            elif b.ymin >= b1ymin:
                                b.appear()
    return cnt,quit_all

if __name__ == '__main__':
    #Basic buttons
    titlebanner = buttonMenu(OPTIONS["DISPLAYSIZE_X"]//2-695,OPTIONS["DISPLAYSIZE_X"]//2+656,25,173,dict_img["img_titlebanner"],"banner")
    exit = buttonMenu(10,5+25*len(dict_str["exit"]),OPTIONS["DISPLAYSIZE_Y"]-50,OPTIONS["DISPLAYSIZE_Y"],dict_img["img_void"],"exit",text=dict_str["exit"],react=reaction_exit)
    
    #Main loop
    while not quitter_jeu:
        b1 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,dict_img["img_button"],"b1",dict_img["img_buttonH"],text=dict_str["campaign_mode"],react=reaction_b1)
        b2 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset,b1ymax+yoffset,dict_img["img_button"],"b2",dict_img["img_button"],dict_img["img_buttonD"],text=dict_str["free_play"]).activation(False)#désactivé par défaut
        b3 = buttonMenu(b1xmin,b1xmax,b1ymin+yoffset*2,b1ymax+yoffset*2,dict_img["img_button"],"b3",dict_img["img_buttonH"],text=dict_str["options"],react=reaction_b3)
    
        while continuer_menu:
            continuer_menu,quitter_jeu = menu_loop()
            if quitter_jeu:
                continuer_menu = False
        continuer_menu = True
    pygame.display.quit()
    pygame.quit()
    #sys.exit(0)
