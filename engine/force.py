from vector import Vector

class Force:
    def __init__(self):
        pass

    def get_speed(self,movablenode):
        pass

class Gravity(Force):
    def __init__(self,g):
        self.__g = g

    def set_g(self,g):
        self.__g = g

    def get_g(self):
        return self.__g
    
    def get_acc(self,movablenode):
        accy = self.get_g()
        return (Vector(0,accy),movablenode.get_ang_acc())

