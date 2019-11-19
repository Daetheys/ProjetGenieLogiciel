#!/usr/bin/env python3

from collideTransformable import CollideTransformable
from vector import Vector

class Node(CollideTransformable):
    """ Node with children """
    def __init__(self):
        super().__init__()
        self.__children = []
        self.__parent = None
        self.__marked_for_removal = False

    def __del__(self):
        for son in self.__children:
            del son

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
        transform = transform*get_transform()
        self.draw_current(transform)
        for child in self.__children:
            child.draw(transform)

    def draw_current(self,fen):
        pass

    def update(self, dt):
        update_current(dt)
        for child in self.__children:
            child.update(dt)

    def update_current(self,dt):
        pass

    def get_absolute_transform(self):
        transform = Transform()
        current = self
        while current is not None:
            transform = transform * current.get_transform()
        return transform

    def get_absolute_position(self):
        return self.get_absolute_transform().transform_vector(Vector())
