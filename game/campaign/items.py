
class Item:
	""" Items of the game:
	has name, picture, type
	"""
	def __init__(self,name='Apple',pic=None,kind=None):
		self.name = name#str, name
		self.pic = pic#pygame.Surface, picture
		self.type = "   "#3-char str: csm for consommable, key, pas, etc..


	def __repr__(self):
		return "Item "+ self.type + ":" + self.name

class Consommable(Item):
	""" self.type = type of an item. Usually strings of len 3."""
	#ItemType, type of the item: consommable, key item, passive item, etc..
	def __init__(self,args=None):
		Item.__init__(self)
		self.effet = args
		self.type = 'csm'

class KeyItem(Item):
	def __init__(self,args=None):
		Item.__init__(self)
		self.key = args#KeyItemIdentifier
		self.type = 'key'

class Passive(Item):
	def __init__(self,args=None):
		Item.__init__(self)
		self.effet = args#PassiveItem Effect
		self.type = 'key'

class Inventory:
	""" Inventory of a character. """
	def __init__(self,items=[]):
		self.items = items#Item list

	def __repr__(self):
		return "Inventory :" + str(self.items)

