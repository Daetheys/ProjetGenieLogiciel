from vector import Vector

class Force:
    """ Force Object """
    def __init__(self):
        pass

    @abstractmethod
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

