
class Cycle:
	""" Cyclic list. Used to display the background video. """
	def __init__(self,l):
		self.l = l
		self.i = 0

	def next(self):
		""" returns the next argument of the list """
		self.i += 1
		if self.i == len(self.l):
				self.i = 0
		return self.l[self.i]

