#!/usr/bin/env python3


'''A Level is the object that contains an instance of the canabalt game. Is can have dialogue, rewards, different conditions for winning and different objects in the \"real\" game. It is n abstract class, each level has its own class for more freedom for level design'''

class Level:    #will be an abstract class -> it is now

    def __init__(self,g):
        self._accessed = False
        self._finished = False

    def set_accessed(self):
        self._accessed = True

    def set_finished(self):
        self._finished = True

    def get_accessed(self):
        return self._accessed

    def get_finished(self):
        return self._finished

    def fun_dialogue(self,g,arg): #à definir dans les classes uniques
        '''display the dialogue corresponding to the arg given and the attributes of the level
        '''
        pass

    def launch(self,g): #à définir dans les classes uniques
        '''the main function of a level
        '''
        pass

    def reward(self,g): #à définir dans les classes uniques
        '''the function that gives the reward
        '''
        pass

    def create_objects(self,g): #à définir dans les classes unqiues
        '''create the objects used in the GameLevel
        '''
        pass

    def check_victory(self,g): #à définir dans les classes uniques
        '''return True if the player passed the level and False otherwise
        '''
        pass