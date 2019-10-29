#!/usr/bin/env python3
from automata import create_automaton

def load_automata():
	"""loads all automata"""
	global dict_ata
	with open("data/json/automata.json", "r") as read_file:
		dict_ata=json.load(read_file,object_hook=create_automaton)

class SpriteSchedule:
    def load_automaton():
		for automat in dict_ata:
			if automat.name == self.name:
				self.ata = automat

    def step(char):
		self.cs = self.tt(self.cs,char)