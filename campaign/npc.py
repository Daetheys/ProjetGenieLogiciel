
class Npc():
	"""Class representing a non-playable character : 
	it has a dialogue"""
	def __init__(self,dial="",to_sell=[]):
		self.dial = dial#str, Dialogue
		self.to_sell = to_sell#Item list, list of saleable items

	def __repr__(self):
		return "NPCharacter :" + self.name

