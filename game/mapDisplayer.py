
import map
import pygame

class MapDisplayer:

    def __init__(self,DISPLAYSIZE_X,DISPLAYSIZE_Y,g):
        """ This class will probably be destroyed in the future."""
        assert False
        self.dx = DISPLAYSIZE_X
        self.dy = DISPLAYSIZE_Y
        self.g = g

    def display(self,map):
        assert False
        self.bg =  pygame.transform.smoothscale(map.image, (self.dx,self.dy))
        self.g.win().blit(self.bg, (0,0))
        for mp in map.get_map_points():
            self.g.win().blit(mp.get_image(), (mp.x,mp.y))
        self.g.flip()

