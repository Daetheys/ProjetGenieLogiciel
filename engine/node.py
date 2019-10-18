#!/usr/bin/env python3

from transformable import Transformable
from vector import Vector

class Node(transformable):
    def __init__(self):
        self.__children = []
        self.__parent = None
        self.__marked_for_removal = False

    def __del__(self):
        for son in self.__children:
            del son

    def get_parent(self):
        return self.__parent()

    def attach_children(self,child):
        if child.__parent.__children is not None:
            child.__parent.__children.remove(child)
        child.__parent = self
        self.__children.append(child)

    def detach_children(self,child):
        if child.__parent is not self:
            return
        child.__parent = None
        self.__children.remove(child)

    def remove_wrecks(self):
        for child in self.__children:
            if child.__marked_for_removal:
                del child

    def stage_for_removal(self):
        self.__marked_for_removal=True

    def is_stage_for_removal(self):
        return self.__marked_for_removal

    def draw(self,transform):
        transform = transform*get_transform()
        self.draw_current(transform)
        for child in self.__children:
            child.draw(transform)

    def draw_current(self,transform):
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
