#!/usr/bin/env python3

from engine.transformable import Transformable
from engine.vector import Vector

""" A node is a bigger object than a Transformable. In fact it represents an architecture of transformable. When a Transform is applied to a node it is also applied to all its children like in a tree. This architecture is not used yet in our project but will be very useful later. """

class Node(Transformable):
    """ Node : Transformable with children """
    def __init__(self):
        super().__init__()
        self.__children = []
        self.__parent = None
        self.__marked_for_removal = False

    def __del__(self):
        """ Delete this node and its children """
        for son in self.__children:
            del son

    def copy(self):
        """ Copies this node """
        n = Node()
        self.paste_in(n)
        return n

    def paste_in(self,n):
        """ Paste this node in n """
        Transformable.paste_in(self,n)

    def get_parent(self):
        """ Returns parent of this node """
        return self.__parent

    def attach_children(self,child):
        """ Attach a node to this """
        #if child.__parent.__children is not None:
        #    child.__parent.__children.remove(child)
        child.__parent = self
        self.__children.append(child)

    def detach_children(self,child):
        """ Detach a node """
        if child.__parent is not self:
            return
        child.__parent = None
        self.__children.remove(child)

    def remove_wrecks(self):
        """ Remove marked to be deleted nodes """
        for child in self.__children:
            if child.__marked_for_removal:
                del child

    def stage_for_removal(self):
        """ Mark this node to be deleted """
        self.__marked_for_removal=True

    def is_stage_for_removal(self):
        """ Returns if a node is marked to be deleted """
        return self.__marked_for_removal

    def translate(self,v):
        """ Override of Transformable.translate -> also translates children """
        super().translate(v)
        for c in self.__children:
            c.translate(v)

    def rotate(self,angle):
        """ Override of Transformable.rotate -> also rotates children """
        super().rotate(angle)
        for c in self.__children:
            c.rotate_around(angle,self)

    def rotate_around(self,angle,n):
        """ Override of Transformable.rotate_around -> also rotates_ardound children """
        super().rotate_around(angle,n)
        for c in self.__children:
            c.rotate_around(angle,n)

    def scale(self,scalex,scaley):
        """ Override of Transformable.scale -> also scales children """
        super().scale(scalex,scaley)
        for c in self.__children:
            c.scale(scalex,scaley)

    def update(self,dt):
        """ Update function -> will be called every frame """
        pass
