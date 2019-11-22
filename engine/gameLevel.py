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

class GameLevel:
    """ Level of the game """
    def __init__(self,objects,player_pos,limgpar=[("data/img/back.jpg",0),("data/img/asteroid.png",1),("data/img/asteroid.png",2)],name=''):
        """ The player spawn in (0,0) """
        self.camera = camera.Camera()
        self.camera.set_position(Vector(-12,-12))
        self.camera.set_dimension(Vector(25,25))
        self.objects = objects
        self.player_pos = player_pos
        self.compute_size_level()
        self.name = name
        self.score = 42

        self.sorted_objects = None
        self.step = None
        self.optimise_data()
        self.time = 0

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
        self.player.set_position(0,-5) #Init pos of the player
        #self.objects.append(self.player) #Player doesn't need to be added to game objects

        #Creation of the gravity
        self.gravity = Gravity(100)
        self.player.add_force(self.gravity)

    def get_camera(self):
        return self.camera

    def get_objects(self):
        return self.objects

    def compute_end_platform_location(self):
        self.end_platform_location = []
        for o in self.get_objects():
            if isinstance(o,SolidPlatform):
                self.end_platform_location.append(o.get_hit_box().get_world_poly().get_max_x())
        self.end_platform_location.sort()

    def optimise_data(self):
        """ Optimise collisions checks and aff """
        #Call it before launching the game of making modification in camera (be carefull it may take a while to execute
        step = self.get_camera().get_dimension().x
        self.step = step
        (minx,maxx,miny,maxy) = self.size_level
        sorted_objects = [[] for i in range( int((maxx-minx)/step) +2)]
        for o in self.objects:
            minposx = o.get_hit_box().get_world_poly().get_min_x()
            maxposx = o.get_hit_box().get_world_poly().get_max_x()
            minindexx = int( (minposx-minx)/step )
            maxindexx = int( (maxposx-minx)/step )+1 #Arrondi au sup
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
        dt = 0.001
        try:
            while True:
                self.main_loop(dt)
        except EndGame as e:
            return (e.issue, e.score)

    def main_loop(self,dt):
        """ Main loop of the game (controllers, physics, ...) """
        pressed = pygame.key.get_pressed()
        #Controller loop
        for event in pygame.event.get() + [None]:
            for o in self.get_objects_opti():
                if o.get_controller() is not None:
                    o.get_controller().execute(event,pressed)
        #Physics
        self.physics_step(dt)
        #Aff
        self.aff()
        #Camera
        self.camera.threeforth_on(self.player)
        #Time
        self.time += dt
        #Score
        while len(self.end_platform_location) > 0 and self.player.get_position().x >= self.end_platform_location[0]:
            del self.end_platform_location[0]
            self.player.add_score(1000)
        #Win / Lose conditions
        (minx,maxx,miny,maxy) = self.get_size_level()
        if self.player.get_position().y > maxy: #C'est inversé :)
            raise EndGame(False,self.score)
        if self.player.get_position().x > maxx:
            raise EndGame(True,self.score)

    def get_objects_opti(self):
        """ Optimise the data structure """
        (minx,maxx,miny,maxy) = self.size_level
        x = self.camera.get_position().x
        index = int((x-minx)/self.step)
        return self.sorted_objects[index]+self.sorted_objects[index+1]+[self.player]

    def physics_step(self,dt):
        """ Compute collisions """
        obj_opti = self.get_objects_opti()
        for o in obj_opti:
            #print(o)
            o.compute_speed(dt)
            o.move()
            if o == self.player:
                #Reposition the player
                pos = o.get_position()
                o.set_position(self.player_pos(self.time),pos.y)
                #Cut X speed (for MAXSPEED)
                speed = self.player.get_speed()
                self.player.set_speed(Vector(0,speed.y))
            for o2 in obj_opti:
                if o != o2 and o.get_hit_box().collide(o2.get_hit_box()):
                    o.collide(o2)
                    o2.collide(o)
                    if o.get_rigid_body() and o2.get_rigid_body() and o.get_rigid_hit_box().collide(o2.get_rigid_hit_box()):
                        #print("------------------rigid",o,o2)
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
