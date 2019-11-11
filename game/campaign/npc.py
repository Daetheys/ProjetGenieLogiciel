import Character

class Npc(Character):
	"""Class representing a non-playable character : 
	it has a dialogue
	Npc (that can talk, sell items, etc..)
	"""
	def __init__(self,name,pic,ctalk=(0,0,0),inv=None,dial=""):
		Character.__init__(self,name,pic,ctalk,inv)
		self.dial = dial#str, Dialogue

	def __repr__(self):
		return "NPCharacter :" + self.name

