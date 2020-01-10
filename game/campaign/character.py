from game.campaign.items import *


class Character():
	"""Class representing a character :
	it has a name,
	a picture,
	talks with a certain color,
	has an inventory"""
	def __init__(self,name,pic,ctalk=(0,0,0),inv={}):
		self.name = name#str, name
		self.pic = pic#pygame.Surface, picture
		self.ctalk = ctalk#int x int x int, color of talk
		self.inv = inv#Inventory, inventory of the character (usually is None)

	def __repr__(self):
		return "Character : " + self.name + "\tSurface:" + str(self.pic) +  "\tColor:" + str(self.ctalk) +  "\tInventory:" + str(self.inv)

	def set_inventory(self,items):
		""" add inventory"""
		for item in items:
			if item.type != 'key':#item.type == "csm":
				self.inv[item] += items[item]
			else:
				self.inv[item] = items[item]

	def get_inventory(self):
		return self.inv

	def is_in_inventory(self,item):
		if self.inv[item] > 0:
			return True
		return False


