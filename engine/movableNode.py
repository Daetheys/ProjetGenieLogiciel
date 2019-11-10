from vector import Vector
from node import Node

class MovableNode(Node):
    """ A node that can move with more powerfull functions"""
    def __init__(self):
        super().__init__()
        self.__speed = Vector(0,0)
        self.__angular_speed = 0
    def set_speed(self,speed):
        self.__speed = speed
    def get_speed(self):
        return self.__speed
    def set_angular_speed(self,speed):
        self.__angular_speed = speed
    def get_angular_speed(self):
        return self.__angular_speed
    def move(self):
        super().translate(self.__speed)
        super().rotate(self.__angular_speed)
        
