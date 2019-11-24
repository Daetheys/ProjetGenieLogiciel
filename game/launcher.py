from buttonMenu import *
from game import *
import pygame
from pygame.locals import *
from tools import score_to_msg
from dialogue import Dialogue
from dialoguebubble import Dialogue_Bubble
from vector import Vector

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
        self.flip()

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
        b_inv = ButtonMenu(self,20,120,20,120,self.dict_img["img_inv"],react = reaction_inv,add_to_list=False)
        b_inv.display()
        list_button.append(b_inv)
        for mp in map.get_map_points():
            if mp.get_accessible():
                self._fenetre.blit(mp.get_image(), (mp.x,mp.y))
                m,M = mp.get_image().get_size()
                list_button.append(ButtonMenu(self,mp.x,mp.x+m,mp.y,mp.y+M,mp.get_image(),react = mp.launch,add_to_list=False))

        self.flip()

        """ event catching zone """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    cnt = False
                    list_button = []
            if event.type == MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if event.button == 1:
                    for b in list_button:
                        if xyinbounds(mx,my,b):
                            cntb,quit_allb = b.react(self)
                            cnt  = cnt and cntb
                            quit_all = quit_all or quit_allb
        return cnt,quit_all

    def dial_loop(self,dial_bubble,cnt = True,quit_all=False,bg = None,map=None,blist=[]):
        pygame.time.Clock().tick(self.options["FPS"])
        dial_bubble.display(self)
        for b in blist:
            if dial_bubble.last:
                b.display(lock=False)
            else:
                b.display(period=5,speed=1,lock=False)
        self.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    cnt = False
                if event.key == K_ESCAPE:
                    cnt = False
                    quit_all = True
            if event.type == MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if event.button == 1:
                    for b in blist:
                        if xyinbounds(mx,my,b):
                            cnt = False
        return cnt,quit_all

    def launch_level(self,gl):
        """ Initializing the main loop of a level,
        where gl is a game level"""

        gl.load_camera(self.win())#Load the camera in the window fen
        gl.get_camera().set_dimension(Vector(200,150)) #Resize the camera
        #2560,1440 (plus grosse résolution)
        gl.get_camera().set_position(Vector(-100,-75)) #change pos of  the camera
        gl.optimise_data() #Call it before launching the game of making modification in camera (be careful it may take a while to execute)
        """
        t = 0#time
        sec_wait = 3#POUR L'INSTANT, 3. SERA UN CHAMP DU GAME_LEVEL(duration) !!
        while t < self.options["FPS"] * sec_wait:
            if not self.loop_level(gl,t):
                return False#on a perdu
        """
        success, score = gl.play(self.options["FPS"])

        if not success:#reduce score of defeats
            score //= 2
        #g.scores[gl.name]  = leaderboard of this level
        self.dict_score[gl.name] = insert_score(self.score(gl.name),score,self.player_name,self.max_number_scores)
        
        msg_score = score_to_msg(self.dict_score[gl.name])
        dial_score = Dialogue([Dialogue_Bubble(msg_score,self.dict_char["narrator"],self.dict_img["img_leaderboard"],300,50,True)])
        dial_score.show(self)

        with open("data/json/scores.json","w") as f:
            f.write(json.dumps(self.dict_score))
        #pour ne pas sortir du menu même si les boutons ont été trop appuyés
        #mashed buttons are handled by pygameeventget (doesn't quit the menu)
        return success#true ssi réussite ! pour l'instant non utilisé. -> maintenant oui !

    def loop_level(self,gl,t):
        """ Running the main loop of a level gl at time t

        This function is obsolete. this loop is now executed in the "GameLevel"
        class"""

        """ #In GameLevel
        pygame.time.Clock().tick(self.options["FPS"])
        #print(t)
        for event in pygame.event.get():
            #Dans cette boucle, on envoie aux Controllers concernés
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False#You failed.
                if event.key == K_UP:
                    print("JUMP!")

        #Updating the camera
        x,y = gl.get_camera().get_position().to_tuple()
        #print((x,y))
        gl.get_camera().set_position(Vector(x+40,y))
        gl.aff()
        #self.flip("SCORE: "+str(t)) #Handled in GameLevel
        t += 1

        #gl.play(t)

        return True
        """
        pass

    def launch_game(self):
        """ Launching the main loop of the main menu"""
        while not self.quitter_jeu:
            b1 = ButtonMenu(self,self.b1xmin,self.b1xmax,self.b1ymin,self.b1ymax,self.dict_img["img_button"],"b1",self.dict_img["img_buttonH"],text=self.dict_str["campaign_mode"],react=reaction_b1)
            b2 = ButtonMenu(self,self.b1xmin,self.b1xmax,self.b1ymin+self.yoffset,self.b1ymax+self.yoffset,self.dict_img["img_button"],"b2",self.dict_img["img_buttonH"],self.dict_img["img_buttonD"],text=self.dict_str["free_play"],react=reaction_b2)
            #b2.activation(False)#activé par défaut -> désactivé par défaut si on le débloque après lvl1?
            b3 = ButtonMenu(self,self.b1xmin,self.b1xmax,self.b1ymin+self.yoffset*2,self.b1ymax+self.yoffset*2,self.dict_img["img_button"],"b3",self.dict_img["img_buttonH"],text=self.dict_str["options"],react=reaction_b3)

            while self.continuer_menu:
                self.continuer_menu,self.quitter_jeu = self.menu_loop()
                if self.quitter_jeu:
                    self.continuer_menu = False
            self.continuer_menu = True
        pygame.display.quit()
        pygame.quit()

