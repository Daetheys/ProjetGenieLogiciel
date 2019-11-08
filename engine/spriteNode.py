from node import Node

class SpriteNode(Node):
	def __init__(self):
		self.__state = None #stay,move,damaged,collision,
		self.__giver = None #

	def set_scheduler(self,sche):
		self.__giver = sche

	def set_state(self,state):
		self.__state = state

	def get_state(self):
		return self.__state
