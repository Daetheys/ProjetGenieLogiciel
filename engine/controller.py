#!/usr/bin/env python3


class Controller:
    """ Controller class (cf Controllable Node) """

    def __init__(self, target=None):
        self._target = target
        self._actions = None

    def get_target(self):
        return self._target

    def set_actions(self,actions):
        self._actions = actions

    def execute(self,event,pressed,dt):
        self.target.update(dt)

