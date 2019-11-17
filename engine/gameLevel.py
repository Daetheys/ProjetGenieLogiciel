import sys
import os
path = os.getcwd()
sys.path.append(path + "/engine")

from camera import Camera
from vector import Vector
import pygame
import time

class GameLevel:
    """ Level of the game """
    def __init__(self,objects,player_pos):
        """ The player spawn in (0,0) """
        self.camera = Camera()
        self.camera.set_position(Vector(0,0))
        self.camera.set_dimension(Vector(10,10))
        self.objects = objects
        self.compute_size_level()

    def get_camera(self):
        return self.camera

    def get_objects(self):
        return self.objects

    def compute_size_level(self):
        """ Computes the size of the level """
        maxi_x = None
        maxi_y = None
        mini_x = None
        mini_y = None
        #Get the rect in which the level is
        for o in self.objects:
            hit_box = o.get_hit_box()
            val_max_x = hit_box.get_max_x()
            val_max_y = hit_box.get_max_y()
            val_min_x = hit_box.get_min_x()
            val_min_y = hit_box.get_min_y()
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
        return self.size_level

    def refresh(self,dt):
        t = time.clock()
        self.physics_step(dt)
        print("ipsp",1/(time.clock()-t))
        self.aff()
        print("ipsf",1/(time.clock()-t))

    def physics_step(self,dt):
        for o in self.get_objects():
            o.compute_speed(dt)
            o.move()
            for o2 in self.get_objects():
                if o != o2 and o.get_hit_box().collide(o2.get_hit_box()):
                    o.collide(o2)
                    o2.collide(o)
                    if o.get_rigid_body() and o2.get_rigid_body() and o.get_rigid_hit_box().collide(o2.get_rigid_hit_box()):
                        #print("------------------rigid",o,o2)
                        o.apply_reaction(o2)

    def load_camera(self,fen):
        self.camera.set_fen(fen)
                        
    def aff(self):
        self.camera.aff(self.objects)
        pygame.display.flip()
