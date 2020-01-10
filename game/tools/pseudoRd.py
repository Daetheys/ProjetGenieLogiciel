
class PseudoRd:
	""" Used to generate campaign levels in a pseudo-random way.
	Only used in the Fantasy campaign"""
	def __init__(self,a,b,c,u):#Put random numbers here except for c but it's better if they are prime numbers
		self.a = a
		self.b = b
		self.c = c #max (maxint-minint)
		self.u = u

	def get(self,minint,maxint):
		self.u = (self.u*self.a+self.b)%self.c
		return self.u%(maxint-minint)+minint

	def __call__(self,*args):
		return self.get(*args)

