#!/usr/bin/env python3
"""
Automata & Sprite Scheduler v2.1.2
-states now are associated to a sprite path
-sprites can be directly loaded in the scheduler
-and states will be associated to a pygame.surface
-load_sprites now works
"""
import json
import pygame
from engine.automata import *

""" A SpriteScheduler is the interface between a SpriteNode and his sprites for animation. It uses an automaton where each state represents an sprite. If the spriteNode is runing for example , its status will be something like 'r' (for run) and each time SpriteScheduler.step(char) is called it will execute transitions in its automaton to get the next sprite of the animation. It's especially usefull because it makes it possible to switch between runing, jumping and death animation for example by adding transitions between those loops """

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
				self.ata = automata.copy()
		if self.ata is None:
			print("Initialization Failed ! name:"+str(self.name),"\n")

	def step(self,char):
		""" does one step of execution of the automaton """
		try:
			self.ata.cs = self.ata.tt[self.ata.cs,char]

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
					self.ata.qn[k] = pygame.image.load(v)
					self.ata.qn[k].convert_alpha(self.ata.qn[k])
				#Somewhere, one loads an automaton once too much as this if is
				#necessary. This can be stopped. We must act immediatly.
		else:
			print("WARNING : You are trying to load already loaded images!")

	def copy(self):
		tau = SpriteScheduler(self.name)
		tau.name = self.name
		tau.ata = self.ata.copy()
		tau.loaded = self.loaded
		return tau


	def __repr__(self):
		return str(self.name)+"\nstates:"+str(self.ata.states)+"\ncs:"+str(self.ata.cs)+"\ntt:"+str(self.ata.tt)
