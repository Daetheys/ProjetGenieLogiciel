"""
Menu 
"""

import pygame
from pygame.display import *
pygame.init()
from pygame.locals import *
pygame.mixer.init()
import sys
def xfil(filename, globals = None, locals = None):
    if globals is None:
        globals = sys._getframe(1).f_globals
    if locals is None:
        locals = sys._getframe(1).f_locals
    with open(filename, "r") as fh:
        exec(fh.read()+"\n", globals, locals)

#Display
FRAMEPERSECONDLIMIT = 30
modeECRAN = FULLSCREEN#modeECRAN = 0 ou FULLSCREEN
DISPLAYSIZE_X = 1600
DISPLAYSIZE_Y = 900
fenetre = pygame.display.set_mode((DISPLAYSIZE_X, DISPLAYSIZE_Y),modeECRAN)#1920*1080
icone = pygame.image.load("_/img/icon.ico")
pygame.display.set_icon(icone)

#Functions
def xyinbounds(mx,my,btn):
    b1xmin,b1xmax,b1ymin,b1ymax = btn.boundaries()
    return b1xmin <= mx and mx <= b1xmax and b1ymin <= my and my <= b1ymax

def T(txt,x,y,r=0,g=0,b=0,aliasing=1,size=20):
    """allows the display of text on screen without centering"""
    font = pygame.font.Font(None, size)
    fenetre.blit(font.render(txt, aliasing, (r, g, b)), (x,y))

def Tex(txt,CenterX=0,CenterY=0,r=0,g=0,b=0,aliasing=1,size=20):
    """allows the display of text on screen with centering"""
    if pygame.font:
        font2 = pygame.font.Font(None, size)
    text = font2.render(txt, aliasing, (r, g, b))
    textpos = text.get_rect(centery=CenterY,centerx=CenterX)
    fenetre.blit(text, textpos)

#will be an active automated gameplay
img_background = pygame.image.load("_/img/Blvr.png").convert_alpha()
img_button = pygame.image.load("_/img/btn/button_menu1.png").convert_alpha()
img_buttonH = pygame.image.load("_/img/btn/button_menu1H.png").convert_alpha()
img_buttonD = pygame.image.load("_/img/btn/button_menu1D.png").convert_alpha()
img_titlebanner = pygame.image.load("_/img/banner.png").convert_alpha()
img_default = pygame.image.load("_/img/default.png").convert_alpha()
img_void = pygame.image.load("_/img/void.png").convert_alpha()

#Title
pygame.display.set_caption("CAN·A·BAELDE")
fenetre.blit(img_background,(0,0))
pygame.display.flip()

#Music
""" menu music is  disabled """
#pygame.mixer.music.load(music_menu)
#pygame.mixer.music.fadeout(500)
#pygame.mixer.music.play(-1)

#Other constants
LANGUAGE = "English"
BUTTON_LIST = []#to keep an eye on all buttons currently displayed
str_campaign_mode = "CAMPAIGN MODE"
str_free_play = "FREE PLAY"
str_options = "OPTIONS"
str_exit = "EXIT"

class buttonMenu:

    def __init__(self,xm,xM,ym,yM,img=img_default,name="Unnamed",picH=None,picD=None,text=None):
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
        else: self.text = text#deactivated
        self.t = 0
        self.up = True
        BUTTON_LIST.append(self)#to keep an eye on all buttons
        self.name = name
        self.speed = 1
        self.period = 1
    def __repr__(self):
        return self.name + '= Button(%s<x<%s, %s<y<%s)\n' % (self.xmin, self.xmax, self.ymin, self.ymax)
    
    def __displayedY(self,yy):
        return yy - self.period//2 + ((self.t//self.speed)%self.period)
         
    def boundaries(self):
        """ returns the visible boundaries of self"""
        return self.xmin,self.xmax,self.__displayedY(self.ymin),self.__displayedY(self.ymax)
    
    def activation(self,flag):self.activated=flag
        
    def display(self,period=None,speed=None,flip=False):
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
            Tex(self.text,(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,size=50)
        else:
            Tex(self.text,(self.xmin+self.xmax)/2,(self.__displayedY(self.ymin)+self.__displayedY(self.ymax))/2,100,100,100,size=50)
        if flip: pygame.display.flip()
        

titlebanner = buttonMenu(105,1456,25,173,img_titlebanner,"banner")
exit = buttonMenu(10,5+20*len(str_exit),DISPLAYSIZE_Y-50,DISPLAYSIZE_Y,img_void,"exit",text=str_exit)

continuer_jeu = True
continuer_menu =  True
continuer_menu_campagne = False
continuer_map  =  False
while continuer_jeu:
    b1xmin = 550
    b1xmax = 1050
    b1ymin = 230
    b1ymax = 400
    b1 = buttonMenu(b1xmin,b1xmax,b1ymin,b1ymax,img_button,"b1",img_buttonH,text=str_campaign_mode)
    b2 = buttonMenu(b1xmin,b1xmax,b1ymin+200,b1ymax+200,img_button,"b2",img_button,img_buttonD,text=str_free_play)
    b2.activation(False)
    b3 = buttonMenu(b1xmin,b1xmax,b1ymin+400,b1ymax+400,img_button,"b3",img_buttonH,text=str_options)

    while continuer_menu:
        pygame.time.Clock().tick(FRAMEPERSECONDLIMIT)
        
        #BACKGROUND DISPLAY
        fenetre.blit(img_background,(0,0))
        
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
                    continuer_menu = False
                    continuer_jeu = False
                if event.key == K_q:
                    continuer_map = True
                if event.key == K_p:
                    pygame.mixer.music.pause()
                if event.key == K_PERIOD:
                    continuer_map = True
            #MOUSE EVENTS HANDLER
            if event.type == MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos() 
                for b in BUTTON_LIST:
                    if xyinbounds(mx,my,b):
                        print(b.name)
                        b.react()
                        if b.name == "b1":#upper button
                            #GO TO CAMPAIGN MODE's MENU
                            xfil("campaign_mode.py")
                        if b.name == "b2":#middle button
                            #GO TO FREE PLAY MODE's MENU
                            pass
                        if b.name == "b3":#lower button
                            #GO TO OPTIONS MODE's MENU
                            pass
                        if b.name == "exit":
                            continuer_menu = False
                            continuer_jeu = False
                        
pygame.display.quit()
pygame.quit()
#sys.exit(0)