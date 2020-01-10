from engine.vector import Vector
from engine.node import Node
from engine.spriteNode import SpriteNode
from engine.polygone import *
from engine.transform import Transform

import pygame
import time

DEBUG = False
MAXMOVE = 10 #Max movement (pixels) per iteration
SHOWCUT = False

""" A Movable Node is the evolution of a SpriteNode. It has a speed and some basic information about physics but no hitbox yet """


class MovableNode(SpriteNode):
    """ A node that can move with more powerful functions"""
    def __init__(self):
        super().__init__()
        self.__speed = Vector(0,0)
        self.__acc = Vector(0,0)
        self.__ang_speed = 0
        self.__ang_acc = 0
        self.__force_effect = {}
        self.__mass = 1 #kg
        self.__ang_inertia = 1 #SI

    def copy(self):
        """ Returns a copy of itself """
        mn = MovableNode()
        self.paste_in(mn)
        return mn

    def paste_in(self,mn):
        """ Paste it in mn """
        SpriteNode.paste_in(self,mn)
        mn.set_speed(self.get_speed())
        mn.set_ang_speed(self.get_ang_speed())
        mn.set_acc(self.get_acc())
        mn.set_ang_acc(self.get_ang_acc())
        mn.set_mass(self.get_mass())
        mn.set_ang_inertia(self.get_ang_inertia())

    def set_mass(self,val):
        self.__mass = val
    def get_mass(self):
        return self.__mass
    def set_ang_inertia(self,val):
        self.__ang_inertia = val
    def get_ang_inertia(self):
        return self.__ang_inertia
    def set_acc(self,val):
        self.__acc = val
    def get_acc(self):
        return self.__acc
    def set_ang_acc(self,val):
        self.__ang_acc = val
    def get_ang_acc(self):
        return self.__ang_acc
    def set_speed(self,speed):
        self.__speed = speed
    def get_speed(self):
        return self.__speed
    def set_ang_speed(self,speed):
        self.__ang_speed = speed
    def get_ang_speed(self):
        return self.__ang_speed

    def set_speedx(self,val):
        speed = self.get_speed()
        self.set_speed(Vector(val,speed.y))
    def set_speedy(self,val):
        speed = self.get_speed()
        self.set_speed(Vector(speed.x,val))

    def add_force(self,force):
        """ Add a force to this node (cf force) """
        self.__force_effect[force] = None
    def affected_by_force(self,force):
        """ Returns True if this node is affected by the given force """
        try:
            self.__force_effect[force]
            return True
        except KeyError:
            return False
    def remove_force(self,force):
        """ Removes the effect of specific force """
        try:
            del self.__force_effect[force]
        except KeyError:
            pass
    def list_forces(self):
        """ Returns the list of forces that affect this node """
        return list(self.__force_effect.keys())
    def move(self,dt):
        """ Moves according to it speed and to the small given time dt. It movement may be cut so that the physics works well """
        v = self.get_speed()*dt
        if v.len() > MAXMOVE:
            if SHOWCUT:
                print("CUT")
            v = self.get_speed().normalise()*MAXMOVE
        #print("translate",self,v)
        self.translate(v)
        self.rotate(self.get_ang_speed())
    def reverse_move(self):
        """ Reverse the last move (not used and shouldn't be)"""
        self.translate(-self.get_speed())
        self.rotate(-self.get_ang_speed())
    def compute_speed(self,dt):
        """ Computes the actual speed according to its acceleration and dt"""
        #Compute acc
        self.compute_effect_forces()
        #Compute speed
        self.set_speed(self.get_speed() + self.get_acc()*dt)
        self.set_ang_speed(self.get_ang_speed() + self.get_ang_acc()*dt)
    def compute_effect_forces(self):
        """ Computes the effect of forces on this node and modify acceleration """
        forces = self.list_forces()
        acc = Vector(0,0)
        ang_acc = 0
        for f in forces:
            (accf,ang_accf) = f.get_acc(self)
            acc += accf
            ang_acc += ang_accf
        self.set_acc(acc/self.get_mass())
        self.set_ang_acc(ang_acc/self.get_ang_inertia())
