
class Item:
	""" Items of the game:
	has name, picture, and type
	"""
	def __init__(self,name='',pic=None):
		self.name = name#str, name
		self.pic = pic#pygame.Surface, picture
		self.type = "   "#3-char str: csm for consommable, key, pas, etc..


	def __repr__(self):
		return "Item "+ self.type + ":" + self.name

	def __hash__(self):
		return hash(self.name)

	def __eq__(self, value):
		""" returns self == value
		note that it is incorrect to have two objects having the same name, but
		not the same type """
		try:
			return self.name == value.name
		except AttributeError:#not an Item
			return False

class Consommable(Item):
	""" Consommable items : Basic items with immediate effects
	an Apple is a consommable.
	self.type = type of an item. Usually strings of len 3."""
	#ItemType, type of the item: consommable, key item, passive item, etc..
	def __init__(self,name,args=None):
		Item.__init__(self,name)
		self.effet = args
		self.type = 'csm'

class KeyItem(Item):
	""" Key Item Class : Used for important items such as Keys and Elven Poems """
	def __init__(self,name,args=None):
		Item.__init__(self,name)
		self.type = 'key'

class Passive(Item):
	""" Passive Item Class : Unused at this moment. """
	def __init__(self,name,args=None):
		Item.__init__(self,name)
		self.effet = args#PassiveItem Effect
		self.type = 'pas'

def item_from_name(name):
	""" creates the item associated to the name 'name' """
	if name == "key_0" or name == "key_A" or name == "key_B":
		return KeyItem(name)
	elif name == "apple" or name == "Apple":
		return Consommable(name)
	else:
		return KeyItem(name)
