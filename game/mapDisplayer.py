
import map
import pygame

class MapDisplayer:

    def __init__(self,DISPLAYSIZE_X,DISPLAYSIZE_Y,fenetre):
        self.dx = DISPLAYSIZE_X
        self.dy = DISPLAYSIZE_Y
        self.fen = fenetre

    def display(self,map):
        self.bg =  pygame.transform.smoothscale(map.image, (self.dx,self.dy))
        self.fen.blit(self.bg, (0,0))
        for mp in map.get_map_points():
            self.fen.blit(mp.get_image(), (mp.x,mp.y))
        pygame.display.flip()

