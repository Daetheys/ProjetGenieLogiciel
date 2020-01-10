import sys
import os
path = os.getcwd()
sys.path.append(path + "/engine")

import camera
from vector import Vector
from background import Background
from parallax import Parallax
from player import Player
from force import Gravity
from solidPlatform import SolidPlatform
from transform import Transform
import pygame
import time
from datetime import datetime

DEBUG = False

def get_current_time():
    return datetime.timestamp(datetime.now())

""" This Class represents a Level of the game : it takes a list of objects (solidPlatform usually) and a position for the player that depends on time """


class GameLevel:
    """ Level of the game """
    def __init__(self,objects,player_pos,limgpar=[("data/img/background_demon_forest/parallax-demon-woods-bg.png",0),("data/img/background_demon_forest/parallax-demon-woods-far-trees.png",1),("data/img/background_demon_forest/parallax-demon-woods-mid-trees.png",2),("data/img/background_demon_forest/parallax-demon-woods-close-trees.png",3)],name='',parallax=True,gravity=2100,music=None):
        """ The player spawn in (0,0) """
        assert objects != [] #Empty GameLevel
        self.camera = camera.Camera() #Camera
        self.camera.set_position(Vector(-12,-12))
        self.camera.set_dimension(Vector(25,25))
        self.objects = objects
        self.player_pos = player_pos
        self.compute_size_level()
        self.name = name

        #Creation of the gravity
        self.gravity = Gravity(gravity) #NOTE POUR LES RAGEUX : On a testé et ca marche bien avec cette valeur -> ca permet d'avoir un saut élegant

        self.begin_time = 0
        self.time = 0 #Time Referential of the level

        #Death animation
        self.lost = False
        self.countdown = 1

        #Creation of the player
        self.player = Player()
        self.player.set_position(0,-16) #Init pos of the player
        self.objects.append(self.player)
        self.player.link_world(self)

        #Camera Y scrolling
        self.camera_y_pos = self.player.get_position().y

        #To optimise physics
        self.sorted_objects = None
        self.dynamic_objects = set([self.player])
        self.opti_step = 10
        self.optimise_data()
        self.progression = 0

        """
        from gravitationalBallShield import GravitationalBallShield
        test_shield = GravitationalBallShield()
        test_shield.link_world(self)
        self.player.add_shield(test_shield)
        
        ppos = self.player.get_position()
        test_shield.set_position(ppos.x,ppos.y)
        self.add_node(test_shield)
        test_shield.generate()
        #self.objects.append(test_shield)
        self.player.attach_children(test_shield)
        """

        #Get end platform locations to compute score
        self.end_platform_location = None
        self.compute_end_platform_location()

        #Load Background
        if not parallax: limgpar = [limgpar[1]] #will be improved later
        lpar = [] #List of Parallax
        for (name,index) in limgpar:
            p = Parallax(name,index) #Create parallax with given speed
            lpar.append(p)

        self.background = Background(lpar)

        for o in objects:
            o.link_world(self)
        
        self.end_init()

        if music != None:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)

    def end_init(self):
        for o in self.objects:
            o.end_init()

    def get_camera(self):
        return self.camera

    def get_objects(self):
        return self.objects

    def load_inventory(self,inv):
        self.player.load_inventory(inv)

    def add_node(self,n):
        """ Adds a new node to the world """
        self.objects.append(n)
        self.dynamic_objects.add(n)
        n.link_world(self)

    def compute_end_platform_location(self):
        """ Compute the list of platform location """
        self.end_platform_location = []
        for o in self.get_objects():
            if isinstance(o,SolidPlatform):
                self.end_platform_location.append(o.get_hit_box().get_world_rect().get_max_x())
        self.end_platform_location.sort()

    def get_objects_opti(self):
        """ Optimise the data structure """
        while self.progression < len(self.sorted_objects):
            o = self.sorted_objects[self.progression]
            orect = o.get_hit_box().get_world_rect()
            crect = self.get_camera().rect
            if orect.collidex(crect):
                self.dynamic_objects.add(o)
                self.progression += 1
            else:
                break
        return self.dynamic_objects

    def optimise_data(self):
        """ Optimise collisions checks and aff """
        #Call it before launching the game of making modification in camera (be carefull it may take a while to execute
        def order(o1):
            return o1.get_hit_box().get_world_rect().get_min_x()
        sorted_objects = self.objects[:]
        sorted_objects.sort(key=order)
        self.sorted_objects = sorted_objects

    def compute_size_level(self):
        """ Computes the size of the level """
        maxi_x = None
        maxi_y = None
        mini_x = None
        mini_y = None
        #Get the rect in which the level is
        for o in self.objects:
            hit_box = o.get_hit_box()
            val_max_x = hit_box.get_world_rect().get_max_x()
            val_max_y = hit_box.get_world_rect().get_max_y()
            val_min_x = hit_box.get_world_rect().get_min_x()
            val_min_y = hit_box.get_world_rect().get_min_y()
            if maxi_x is None or val_max_x > maxi_x:
                maxi_x = val_max_x
            if mini_x is None or val_min_x < mini_x:
                mini_x = val_min_x
            if maxi_y is None or val_max_y > maxi_y:
                maxi_y = val_max_y
            if mini_y is None or val_min_y < mini_y:
                mini_y = val_min_y
        self.size_level = (mini_x,maxi_x,mini_y,maxi_y)

    def get_size_level(self):
        """ Returns the size of the level as a tuple (minx,maxx,miny,maxy) """
        return self.size_level

    def play(self,fps):
        """ Launches the gameLevel , returns +score if win, -score if lose """
        t0 = get_current_time()
        tn = t0
        try:
            while True:
                #Get time
                now = get_current_time()
                #Compute dt from previous iteration
                dt = now-tn
                #Updates time from the begining
                self.time = tn-t0
                #Launch the loop
                self.main_loop(dt)
                #Updates tn for the next iteration
                tn = now

        except EndGame as e:
            #print("--",time.clock()-t0,self.time)
            return (e.issue, e.score)

    def main_loop(self,dt):
        #to = time.clock()
        """ Main loop of the game (controllers, physics, ...) """
        self.animation_end_game(dt)
        obj_opti = set(self.get_objects_opti())
        self.compute_controller(obj_opti,dt)
        self.physics_step(dt,obj_opti)
        #Camera set position (3/4)
        self.compute_camera_position(obj_opti)
        #Show all sprites
        self.aff(dt,obj_opti)
        #print("aff",time.clock()-t)
        #Score
        self.compute_score()
        #Win / Lose conditions
        self.compute_win_lose()
        #print("fps",1/(time.clock()-to))
        
        #To slow the game
        #time.sleep(0.05)

    def animation_end_game(self,dt):
        if self.lost:
            if self.countdown > 0:
                self.countdown -= dt
            else:
                raise EndGame(False,self.player.score)

    def compute_camera_position(self,obj_opti):
        prect = self.player.get_hit_box().get_world_rect()
        mini = None
        for o in obj_opti:
            if isinstance(o,SolidPlatform):
                rect = o.get_hit_box().get_world_rect()
                if rect.collidex(prect):
                    y = rect.get_min_y()
                    if (mini is None and prect.get_min_y() < y or prect.get_min_y() < y < mini) and abs(prect.get_min_y()-y)<100:
                        mini = y
        if mini is None:
            y = self.player.get_position().y
        else:
            y = mini

        old_percent = 95 #The percentage of the old value of self.camera_y_pos that will be kept
        self.camera_y_pos = self.camera_y_pos*old_percent/100+y*(100-old_percent)/100 #Computation of the new continous Y position of the camera
        self.camera.threeforth_on(Vector(self.player.get_position().x,self.camera_y_pos)) #Position of the camera (pos X of the player et pos Y previously computed)
        

    def compute_win_lose(self):
        """ Compute win / lose conditions """
        (minx,maxx,miny,maxy) = self.get_size_level()
        if self.player.get_position().y > maxy or not(self.player.alive): #C'est inversé :)
            self.lose()
        #if self.player.get_position().x > maxx:
        #    self.win()

    def compute_score(self):
        """ Compute score """
        while len(self.end_platform_location) > 0 and self.player.get_position().x >= self.end_platform_location[0]:
            del self.end_platform_location[0]
            self.player.add_score(1000)

    def compute_controller(self,objects,dt):
        """ Compute controllers """
        pressed = pygame.key.get_pressed()
        #Controller loop
        for event in pygame.event.get() + [None]:
            for o in set(objects):
                if o.get_controller() is not None:
                    o.get_controller().execute(event,pressed,dt)
        #Physics

    def win(self):
        """ Win the game """
        self.player.flush_score()
        raise EndGame(True,self.player.score)

    def lose(self):
        """ Lose the game """
        self.player.flush_score()
        self.lost = True

    def physics_step(self,dt,obj_opti):
        """ Compute collisions """
        for i,o in enumerate(obj_opti):
            if True:#not(isinstance(o,SolidPlatform)): #On peut se permettre d'integrer les plateformes au calcul suite a de nombreux gains de performance
                o.compute_speed(dt)
                o.move(dt)
                if o == self.player and self.player.alive:
                    #Reposition the player
                    pos = o.get_position()
                    new_pos = Vector(self.player_pos(self.time),pos.y)
                    o.translate(new_pos-pos)

                    #Cut X speed (for MAXSPEED)
                    speed = self.player.get_speed()
                    self.player.set_speed(Vector(1,speed.y)) #Player needs to have a str pos speed
                for j,o2 in enumerate(obj_opti):
                    if o.get_collide() and o2.get_collide():
                        coll = o.get_hit_box().collide_sides(o2.get_hit_box())
                        #print("--",o,o2,coll)
                        if o != o2 and coll:
                            o.collide(o2,coll,(coll+2)%4)
                            o2.collide(o,(coll+2)%4,coll)
                            while o.get_rigid_body() and o2.get_rigid_body() and o.get_rigid_hit_box().collide(o2.get_rigid_hit_box()) and o.get_speed() != Vector(0,0):
                                #print("rigid")
                                o.apply_solid_reaction(o2)

    def load_camera(self,fen):
        """ Loads the actual camera of the Level """
        self.background.load(fen) #Loads the background too
        self.camera.set_fen(fen)
        self.camera.link_world(self)

    def get_background(self):
        return self.background

    def set_background(self,v):
        self.background = v

    def aff(self,dt,objects):
        """ Aff all objects that are in the camera of this """
        self.camera.aff(objects,self.get_background(),self.player.get_score(),dt)
        pygame.display.flip()

class EndGame(Exception):
    def __init__(self,issue,score):
        self.issue = issue
        self.score = score
