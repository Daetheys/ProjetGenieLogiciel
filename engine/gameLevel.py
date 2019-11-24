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
import pygame
import time
from datetime import datetime

DEBUG = False

def get_current_time():
    return datetime.timestamp(datetime.now())

class GameLevel:
    """ Level of the game """
    def __init__(self,objects,player_pos,limgpar=[("data/img/background/parallax-demon-woods-bg.png",0),("data/img/background/parallax-demon-woods-far-trees.png",1),("data/img/background/parallax-demon-woods-mid-trees.png",2),("data/img/background/parallax-demon-woods-close-trees.png",3)],name=''):
        """ The player spawn in (0,0) """
        assert objects != [] #Empty GameLevel -> Check your arguments it's not Nicolas's fault if you give an empty gameLevel
        self.camera = camera.Camera()
        self.camera.set_position(Vector(-12,-12))
        self.camera.set_dimension(Vector(25,25))
        self.objects = objects
        self.player_pos = player_pos
        self.compute_size_level()
        self.name = name

        self.begin_time = 0
        self.time = 0

        self.score = 42 #To be removed after merge branch

        #Death animation
        self.lost = False
        self.countdown = 30

        #To optimise physics
        self.sorted_objects = None
        self.opti_step = 10
        self.optimise_data()

        #Get end platform locations to compute score
        self.end_platform_location = None
        self.compute_end_platform_location()

        #Load Background
        lpar = [] #List of Parallax
        for (name,index) in limgpar:
            p = Parallax(name,index) #Create parallax with given speed
            lpar.append(p)
            
        self.background = Background(lpar)

        #Creation of the player
        self.player = Player()
        self.player.set_position(0,-16) #Init pos of the player
        #self.objects.append(self.player) #Player doesn't need to be added to game objects

        #Creation of the gravity
        self.gravity = Gravity(60*35)
        self.player.add_force(self.gravity)

    def get_camera(self):
        return self.camera

    def get_objects(self):
        return self.objects

    def load_inventory(self,inv):
        self.player.load_inventory(inv)

    def compute_end_platform_location(self):
        self.end_platform_location = []
        for o in self.get_objects():
            if isinstance(o,SolidPlatform):
                self.end_platform_location.append(o.get_hit_box().get_world_poly().get_max_x())
        self.end_platform_location.sort()

    def optimise_data(self):
        """ Optimise collisions checks and aff """
        #Call it before launching the game of making modification in camera (be carefull it may take a while to execute
        step = self.opti_step #self.get_camera().get_dimension().x
        (minx,maxx,miny,maxy) = self.size_level
        sorted_objects = [[] for i in range( int((maxx-minx)/step+0.5) +1)]
        for o in self.objects:
            minposx = o.get_hit_box().get_world_poly().get_min_x()
            maxposx = o.get_hit_box().get_world_poly().get_max_x()
            minindexx = int( (minposx-minx)/step )
            maxindexx = int( (maxposx-minx)/step ) #Arrondi au sup
            for i in range(minindexx,maxindexx+1): #On va jusqu'au max inclu
                sorted_objects[i].append(o)
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
            val_max_x = hit_box.get_world_poly().get_max_x()
            val_max_y = hit_box.get_world_poly().get_max_y()
            val_min_x = hit_box.get_world_poly().get_min_x()
            val_min_y = hit_box.get_world_poly().get_min_y()
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
        #self.begin_time = get_current_time()
        #self.time = self.begin_time
        #r = 0 #If an iteration is too long, this time will be put here to be added to next iteration
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
                #print(now,dt,self.time)
                #Launch the loop
                self.main_loop(dt)
                #Updates tn for the next iteration
                tn = now
                #t2 = time.clock()-t
                #time_wait = 1/fps-t2
                #if time_wait < 0:
                #    r = time_wait #We are late !
                #else:
                #    time.sleep(time_wait) #Everything is ok
                #    r = 0
                #pygame.time.Clock().tick(1/fps-t2)
                #print(1/(time.clock()-t),dt,self.time)
                
        except EndGame as e:
            #print("--",time.clock()-t0,self.time)
            return (e.issue, e.score)

    def main_loop(self,dt):
        #new_time = get_current_time()
        #dt = new_time - self.time
        #self.time = new_time - self.begin_time
        """ Main loop of the game (controllers, physics, ...) """
        if self.lost:
            if self.countdown > 0:
                self.countdown -= 1
            else:
                raise EndGame(False,self.player.score)
        self.compute_controller()
        self.physics_step(dt)
        #Camera set position (3/4)
        self.camera.threeforth_on(Vector(self.player_pos(self.time),self.player.get_position().y))
        #Aff
        self.aff()
        #Score
        self.compute_score()
        #Win / Lose conditions
        self.compute_win_lose()

    def compute_win_lose(self):
        (minx,maxx,miny,maxy) = self.get_size_level()
        if self.player.get_position().y > maxy or not(self.player.alive): #C'est inversé :)
            self.lose()
        if self.player.get_position().x > maxx:
            self.win()

    def compute_score(self):
        while len(self.end_platform_location) > 0 and self.player.get_position().x >= self.end_platform_location[0]:
            del self.end_platform_location[0]
            self.player.add_score(1000)

    def compute_controller(self):
        pressed = pygame.key.get_pressed()
        #Controller loop
        for event in pygame.event.get() + [None]:
            for o in self.get_objects_opti():
                if o.get_controller() is not None:
                    o.get_controller().execute(event,pressed)
        #Physics

    def win(self):
        raise EndGame(True,self.player.score)

    def lose(self):
        self.lost = True

    def get_objects_opti(self):
        """ Optimise the data structure """
        (minx,maxx,miny,maxy) = self.size_level
        x = self.camera.get_position().x
        index = int((x-minx)/self.opti_step)
        set_opti = set()
        nb = int(self.camera.get_dimension().x/self.opti_step+0.5)+1
        for i in range(nb):
            if index+i < len(self.sorted_objects):
                set_opti |= set(self.sorted_objects[index+i])
        return set_opti | set([self.player])

    def physics_step(self,dt):
        """ Compute collisions """
        obj_opti = self.get_objects_opti()
        if DEBUG:
            print("---")
            print("player rigid",self.player.get_rigid_hit_box())
            for plat in obj_opti:
                print("plat",plat,plat.get_rigid_hit_box())
        for o in obj_opti:
            #print(o)
            o.compute_speed(dt)
            o.move(dt)
            if o == self.player and self.player.alive:
                #Reposition the player
                pos = o.get_position()
                o.set_position(self.player_pos(self.time),pos.y)

                #Cut X speed (for MAXSPEED)
                speed = self.player.get_speed()
                self.player.set_speed(Vector(1,speed.y)) #Player need to have a str pos speed
            for o2 in obj_opti:
                #print("collide")
                if o.get_hit_box().collide(o2.get_hit_box()):
                    coll,coll2 = o.get_hit_box().collide_sides(o2.get_hit_box())
                    if o != o2 and (coll or coll2):
                        if DEBUG:
                            print("collide",o,o2)
                            print("o",o.get_hit_box(),o.get_rigid_hit_box())
                            print("o2",o2.get_hit_box(),o2.get_rigid_hit_box())
                        o.collide(o2,coll,coll2)
                        o2.collide(o,coll2,coll)
                        while o.get_rigid_body() and o2.get_rigid_body() and o.get_rigid_hit_box().collide(o2.get_rigid_hit_box()) and o.get_speed() != Vector(0,0):
                            if DEBUG:
                                print("rigid")
                            o.apply_solid_reaction(o2)

    def load_camera(self,fen):
        """ Loads the actual camera of the Level """
        self.background.load(fen) #Loads the background too
        self.camera.set_fen(fen)

    def get_background(self):
        return self.background

    def set_background(self,v):
        self.background = v

    def aff(self):
        """ Aff all objects that are in the camera of this """
        self.camera.aff(self.get_objects_opti(),self.get_background(),self.player.get_score())
        pygame.display.flip()

class EndGame(Exception):
    def __init__(self,issue,score):
        self.issue = issue
        self.score = score
