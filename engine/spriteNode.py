from node import Node
import pygame
from vector import Vector
from spriteScheduler import SpriteScheduler

class SpriteNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.__state = None #stay,move,damaged,collision,
        self.__sps = None #

    def set_sps(self,sche):
        self.__sps = sche

    def create_sps(self,name):
        """
        creates the SpriteScheduler associated with the name "name"
        to add/modify such a SpriteScheduler,
        feel free to change the corresponding json.
        """
        sche = SpriteScheduler(name)
        sche.load_automaton()
        sche.load_sprites()
        self.__sps = sche

    def get_sps(self):
        """ returns the spriteScheduler associated with the spriteNode"""
        return self.__sps

    def set_state(self,state):
        self.__state = state

    def get_state(self):
        return self.__state

    def aff(self,fen,distorsion):
        if  self.__sps is not None:
            if self.__sps.loaded:
                img = self.__sps.get_sprite()
            else:
                s = self.__sps.get_sprite()
                img = pygame.image.load(s).convert_alpha()
            image_dim = Vector(img.get_width(),img.get_height())
            scale,trans = distorsion
            dist = scale.transform_vect(image_dim)
            img = pygame.transform.smoothscale(img,dist)
            pos = self.get_position()
            pos.apply_transform(scale)
            pos.apply_transform(trans)
            fen.blit(img,(pos.x ,pos.y ))
        if True:
            pygame.draw.polygon(fen,(0,255,0),(self.get_hit_box().apply_transform(scale).apply_transform(trans)).to_tuples())
            pygame.draw.polygon(fen,(188,0,0),(self.get_rigid_hit_box().apply_transform(scale).apply_transform(trans)).to_tuples())
