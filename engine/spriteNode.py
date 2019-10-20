from node import Node

class SpriteNode(Node):
	def __init__(self):
		self.__state = None #stay,move,damaged,collision,
		self.__giver = None
		