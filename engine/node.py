#!/usr/bin/env python3

from transformable import Transformable
from vector import Vector

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
        if child.__parent.__children is not None:
            child.__parent.__children.remove(child)
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

    def draw(self,transform):
        """ Computes transformations on everyone """
        self.draw_current(transform)
        transform = transform.combine(self.get_transform())
        for child in self.__children:
            child.draw(transform)

    def draw_current(self,tr):
        """ Compute things on this node (because it's not used yet this method is empty but will contain all useful stuff - depending on what we'll need later) """
        self.apply_transform(tr)

    def update(self, dt):
        """ Same concept than draw but to compute dynamic information """
        self.update_current(dt)
        for child in self.__children:
            child.update(dt)

    def update_current(self,dt):
        """ Also empty ... for now """
        pass

    """ #Not Used yet but will represent the stack of transformation of children that may impact the parent """
    def get_absolute_transform(self):
        transform = Transform()
        current = self
        while current is not None:
            transform = transform * current.get_transform()
        return transform

    def get_absolute_position(self):
        return self.get_absolute_transform().transform_vector(Vector())
