#!/usr/bin/env python3


class Controller:
    """ Controller class (cf Controllable Node) """

    def __init__(self, target=None):
        self._target = target

    def get_target(self):
        """ Returns the target of this controller """
        return self._target

    def execute(self,event,pressed,dt):
        """ Executes the controller for inputs [event] and [pressed] keys for the delta time dt"""
        self.target.update(dt)

