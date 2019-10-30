#!/usr/bin/env python3
import sys
import os
import json

path = os.getcwd()
print(path)
path += "/engine"#pour import automata
sys.path.append(path)
from automata import *

class SpriteScheduler:
	def __init__(self,name=""):
		"""
		initialization of the SpriteSchedule, with the sprite name, and no automaton
		"""
		self.name = name
		self.ata = None

	def load_automaton(self):
		"""
		loads in dict_ata the automaton whose name matches self's
		"""
		for automata in dict_ata.values():
			if automata.name == self.name:
				self.ata = automata

	def step(self,char):
		""" does one step of execution of the automaton """
		try:
			self.ata.cs = self.ata.tt[self.ata.cs,char]
			return True
		except TransitionUndefined:
			print("No transition from state "+str(self.ata.cs)+" with letter "+char+".")
			raise TransitionUndefined

	def __repr__(self):
		return str(self.name)+"\nstates:"+str(self.ata.states)+"\ncs:"+str(self.ata.cs)+"\ntt:"+str(self.ata.tt)
