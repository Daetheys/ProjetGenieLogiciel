#!/usr/bin/env python3
"""
Automata & Sprite Scheduler v2.1.2
-states now are associated to a sprite path
-sprites can be directly loaded in the scheduler
-and states will be associated to a pygame.surface
-load_sprites now works
"""
import sys
import os
import json
import pygame

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
		self.loaded = False

	def load_automaton(self):
		"""
		loads in dict_ata the automaton whose name matches self's
		"""
		for automata in dict_ata.values():
			if automata.name == self.name:
				self.ata = automata
		if self.ata is None:
			print("Initialization Failed ! name:"+str(self.name))

	def step(self,char):
		""" does one step of execution of the automaton """
		try:
			self.ata.cs = self.ata.tt[self.ata.cs,char]
			return True
		except TransitionUndefined:
			print("No transition from state "+str(self.ata.cs)+" with letter "+char+".")
			raise TransitionUndefined

	def get_sprite(self):
		"""
		Returns the current sprite.
		"""
		return self.ata.qn[self.ata.cs]

	def load_sprites(self):
		"""
		After a call to sps.load_sprites(), sps.get_sprite() directly returns
		the Pygame.surface object, and not the mere string 'path-to-image'
		"""
		if not self.loaded:
			self.loaded = True
			for k,v in self.ata.qn.items():
				if type(v) == type(""):
					self.ata.qn[k] = pygame.image.load(v).convert_alpha()
				#Somewhere, one loads an automaton once too much as this if is
				#necessary. This can be stopped. We must act immediatly.
		else:
			print("WARNING : You are trying to load already loaded images!")


def __repr__(self):
		return str(self.name)+"\nstates:"+str(self.ata.states)+"\ncs:"+str(self.ata.cs)+"\ntt:"+str(self.ata.tt)
