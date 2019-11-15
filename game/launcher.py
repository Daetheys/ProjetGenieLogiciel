from buttonMenu import *
from game import *
import pygame
from pygame.locals import *

class Launcher(Game):

    def __init__(self):
        """ The Launcher class continues initialization (that Game began), initialises
        all button-related activities, and launches the main loop"""
        Game.__init__(self)
        self.init_buttons()
        self.launch_game()

    def init_buttons(self):
        """ creates some initially displayed buttons"""
        #Basic buttons
        self.titlebanner = ButtonMenu(self,self.options["DISPLAYSIZE_X"]//2-695,self.options["DISPLAYSIZE_X"]//2+656,25,173,self.dict_img["img_titlebanner"],"banner")
        self.exit = ButtonMenu(self,10,5+25*len(self.dict_str["exit"]),self.options["DISPLAYSIZE_Y"]-50,self.options["DISPLAYSIZE_Y"],self.dict_img["img_void"],"exit",text=self.dict_str["exit"],react=reaction_exit)

    def menu_loop(self,cnt = True,quit_all=False,background = None,scrolling=False,scrollist=[]):
        """
        function used for various loops. returns:
        continue (whether the loop nesting it stops)
        quit_all (whether the full game stops)
        """
        if background == None:
            background = self.dict_img["img_background"]
        global BUTTON_LIST
        pygame.time.Clock().tick(self.options["FPS"])

        #BACKGROUND DISPLAY
        self._fenetre.blit(background,(0,0))

        #BUTTON DISPLAY
        for b in BUTTON_LIST:
            if b.name == "banner":
                b.display(5,3)
            elif b.name == "exit":
                b.display(1,1)
            else:
                b.display(20)
        if scrolling and len(scrollist):
            if scrollist[-1].ymax > self.b1ymax+400:
                self._fenetre.blit(self.dict_img["img_arrow"],(self.options["DISPLAYSIZE_X"]//2+250,300))
            else:
                self._fenetre.blit(self.dict_img["img_garrow"],(self.options["DISPLAYSIZE_X"]//2+250,300))
            if scrollist[0].ymin < self.b1ymin:
                self._fenetre.blit(pygame.transform.flip(self.dict_img["img_arrow"],False,True),(self.options["DISPLAYSIZE_X"]//2+250,250))
            else:
                self._fenetre.blit(pygame.transform.flip(self.dict_img["img_garrow"],False,True),(self.options["DISPLAYSIZE_X"]//2+250,250))
        pygame.display.flip()

        #KEYBOARD HANDLER
        #keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit_all = True
                    cnt = False
                if event.key == K_p:
                    #pygame.mixer.music.pause() music disabled
                    pass
            #MOUSE EVENTS HANDLER
            if event.type == MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if event.button == 1:
                    for b in BUTTON_LIST:
                        if xyinbounds(mx,my,b):
                            print(b.name)
                            #print(b.react)
                            cntb,quit_allb = b.react(self)
                            cnt  = cnt and cntb
                            quit_all = quit_all or quit_allb

                if scrolling and len(scrollist):
                    if event.button == 5:
                        if scrollist[-1].ymax > self.b1ymax+400:
                            #empeche d'aller trop loin en bas
                            #print("scroll up")
                            for b in scrollist:
                                b.ymin -= self.yoffset
                                b.ymax -= self.yoffset
                                if b.ymin < self.b1ymin:
                                    if b.visible:
                                        b.disappear()
                                elif b.ymax <= self.b1ymax+400:
                                    b.appear()
                    elif event.button == 4:
                        if scrollist[0].ymin < self.b1ymin:
                            #empeche d'aller trop loin en haut
                            #print("scroll down")
                            for b in scrollist:
                                b.ymin += self.yoffset
                                b.ymax += self.yoffset
                                if b.ymax > self.b1ymax+400:
                                    if b.visible:
                                        b.disappear()
                                elif b.ymin >= self.b1ymin:
                                    b.appear()
        return cnt,quit_all

    def map_loop(self,cnt = True,quit_all=False,bg = None,map=None):
        """loop of a map menu
        displays all accessible map_points in map, over the map's image
        """
        pygame.time.Clock().tick(self.options["FPS"])
        if bg is None: bg = self.dict_img["img_background"]
        if map is None: return cnt,quit_all
        self._fenetre.blit(bg, (0,0))
        list_button = []
        for mp in map.get_map_points():
            self._fenetre.blit(mp.get_image(), (mp.x,mp.y))
            m,M = mp.get_image().get_size()
            list_button.append(ButtonMenu(self,mp.x,mp.x+m,mp.y,mp.y+M,mp.get_image(),react = mp.launch,add_to_list=False))

        pygame.display.flip()

        """ event catching zone """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    cnt = False
                    for i in range(len(list_button)):
                        del list_button[i]
            if event.type == MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if event.button == 1:
                    for b in list_button:
                        if xyinbounds(mx,my,b):
                            cntb,quit_allb = b.react(self)
                            cnt  = cnt and cntb
                            quit_all = quit_all or quit_allb
        return cnt,quit_all

    def dial_loop(self,cnt = True,quit_all=False,bg = None,map=None):
        pygame.time.Clock().tick(self.options["FPS"])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    cnt = False
                if event.key == K_ESCAPE:
                    cnt = False
                    quit_all = True
        return cnt,quit_all

    def launch_game(self):
        """ Launching the main loop """
        while not self.quitter_jeu:
            b1 = ButtonMenu(self,self.b1xmin,self.b1xmax,self.b1ymin,self.b1ymax,self.dict_img["img_button"],"b1",self.dict_img["img_buttonH"],text=self.dict_str["campaign_mode"],react=reaction_b1)
            b2 = ButtonMenu(self,self.b1xmin,self.b1xmax,self.b1ymin+self.yoffset,self.b1ymax+self.yoffset,self.dict_img["img_button"],"b2",self.dict_img["img_button"],self.dict_img["img_buttonD"],text=self.dict_str["free_play"])
            b2.activation(False)#désactivé par défaut
            b3 = ButtonMenu(self,self.b1xmin,self.b1xmax,self.b1ymin+self.yoffset*2,self.b1ymax+self.yoffset*2,self.dict_img["img_button"],"b3",self.dict_img["img_buttonH"],text=self.dict_str["options"],react=reaction_b3)

            while self.continuer_menu:
                self.continuer_menu,self.quitter_jeu = self.menu_loop()
                if self.quitter_jeu:
                    self.continuer_menu = False
            self.continuer_menu = True
        pygame.display.quit()
        pygame.quit()

