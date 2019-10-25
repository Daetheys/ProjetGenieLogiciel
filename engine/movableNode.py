class MovableNode:
    """ A node that can move with more powerfull functions"""
    def __init__(self):
        self.__speed = 0
    def set_speed(self,speed):
        self.__speed = speed
    def get_speed(self):
        return self.__speed
