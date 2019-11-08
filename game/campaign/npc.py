import Character

class Npc(Character):
	"""Class representing a non-playable character : 
	it has a dialogue
	Npc (that can talk, sell items, etc..)
	"""
	def __init__(self,super,dial="",to_sell=[]):
		Character.__init__(self)
		self.dial = dial#str, Dialogue
		self.to_sell = to_sell#Item list, list of saleable items

	def __repr__(self):
		return "NPCharacter :" + self.name

