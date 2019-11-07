
class Character():
	"""Class representing a character : 
	it has a name,
	 a picture,
	 talks with a certain color,
	 has an inventory
	 if it is an npc, there is a link to the corresponding class """
	def __init__(self,name,pic,ctalk=(0,0,0),inv=None,npc=None):
		self.name = name#str, name
		self.pic = pic#pygame.Surface, picture
		self.ctalk = ctalk#int x int x int, color of talk
		self.inv = inv#Inventory, inventory of the character (usually is None)
		self.npc = npc#Npc, link to the corresponding npc (that can talk, sell items, etc..)

	def __repr__(self):
		return "Character :" + self.name

