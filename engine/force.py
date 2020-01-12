from engine.vector import Vector



class Force:
    """ A force is something that can influence a MovableNode by modifying its acceleration """
    """ Force Object : Abstract Class"""
    def __init__(self):
        pass

    def get_acc(self,movablenode):
        pass

class Gravity(Force):
    """ Simple gravity """
    def __init__(self,g):
        self.__g = g #Simple Gravity 

    def set_g(self,g):
        """ Sets g """
        self.__g = g

    def get_g(self):
        """ Returns g """
        return self.__g

    def get_acc(self,movablenode):
        """ Computes the acceleration of the movableNode """
        accy = self.get_g()
        return (Vector(0,accy)*movablenode.get_mass(),movablenode.get_ang_acc())
