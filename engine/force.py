from vector import Vector

class Force:
    """ Force Object """
    def __init__(self):
        pass

    def get_acc(self,movablenode):
        pass

class Gravity(Force):
    def __init__(self,g):
        self.__g = g

    def set_g(self,g):
        """ Sets g """
        self.__g = g

    def get_g(self):
        """ Returns g """
        return self.__g
    
    def get_acc(self,movablenode):
        """ Computes the acceleration of the movableNode """
        accy = self.get_g()
        return (Vector(0,accy),movablenode.get_ang_acc())

class Jump(Force):
    def __init__(self,strength):
        self.strength = strength

    def set_strength(self,val):
        self.strength = val

    def get_strength(self):
        return self.strength

    def get_acc(self,movablenode):
        return (Vector(0,-self.strength*movablenode.get_mass()),0)
