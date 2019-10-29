#!/usr/bin/env python3
from automata import *

def load_automata():
	"""loads all automata"""
	global dict_ata
	with open("../data/json/automata.json", "r") as read_file:
		dict_ata = json.load(read_file,object_hook=create_automaton)

class SpriteSchedule:
	def __init__(self,name=""):
		self.name = name
		self.ata = None
	def load_automaton(self):
		for automat in dict_ata:
			if automat.name == self.name:
				self.ata = automat

	def step(self,char):
		try:
			self.ata.cs = self.ata.tt[self.ata.cs,char]
		except TransitionUndefined:
			print("No transition from state"+str(self.ata.cs)+"with letter"+char)
