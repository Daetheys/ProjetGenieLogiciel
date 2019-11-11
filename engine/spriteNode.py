from node import Node
import pygame

class SpriteNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.__state = None #stay,move,damaged,collision,
        self.__sps = None #

    def set_sps(self,sche):
        self.__sps = sche

    def get_sps(self):
        return self.__sps

    def set_state(self,state):
        self.__state = state

    def get_state(self):
        return self.__state

    def aff(self,fen):
        s = self.__sps.get_sprite()
        img = pygame.image.load(s).convert_alpha()
        pos = self.get_position()
        fen.blit(img,(pos.x,pos.y))
