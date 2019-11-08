
class Consommable(Item):
	""" Type of an item. Usually strings of len 3."""
	#ItemType, type of the item: consommable, key item, passive item, etc..
	def __init__(self,kind,args=None):
		Item.__init__(self)
		self.kind = kind#3-char str: con for consommable, key, pas, etc..

class Item:
	""" Items of the game:
	has name, picture, type
	"""
	def __init__(self,name='Apple',pic=None,kind=None):
		self.name = name#str, name
		self.pic = pic#pygame.Surface, picture
		

	def __repr__(self):
		return "Item :" + self.name + " of type :" +  self.kind

class Inventory:
	""" Inventory of a character. """
	def __init__(self,items=[]):
		self.items = items#Item list

	def __repr__(self):
		return "Inventory :" + str(self.items)

