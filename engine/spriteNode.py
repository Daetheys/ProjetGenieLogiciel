from node import Node
import pygame
from vector import Vector

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

    def aff(self,fen,distorsion):
        s = self.__sps.get_sprite()
        img = pygame.image.load(s).convert_alpha()
        image_dim = Vector(img.get_width(),img.get_height())
        dist = distorsion.transform_vect(image_dim)
        #img = pygame.transform.smoothscale(img,dist)
        pos = self.get_position()
        #fen.blit(img,(pos.x*distorsion.x,pos.y*distorsion.y))
        pygame.draw.polygon(fen,(0,255,0),(self.get_hit_box().apply_transform(distorsion)).to_tuples())
        pygame.draw.polygon(fen,(255,0,0),(self.get_rigid_hit_box().apply_transform(distorsion)).to_tuples())
