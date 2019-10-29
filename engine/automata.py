#!/usr/bin/env python3
from os import getcwd
from sys import path
path0 = getcwd()
path0 += "/error"
path.append(path)
from exception import TransitionUndefined

class Automata:
	def __init__(self,name,states,tt,cs):
		self.name = name
		self.states = states
		self.tt = tt#transition table
		self.cs = cs#current state

def create_automaton(data,name=None,states=None,tt=None,cs=None,jsonparse=True):
	"""creates an automaton:
		- from the json parser if jsonparse
		- from the explicitly given data else

	json parser format :  name|n|tt : where
		name(str) is the name
		n	(int) is the number of states
		tt	(str) is of the following format:
			s,a → b; t,c → q
			
	note : the initial state is always set to 0 in a json parser
	"""
	def newfun(f,old_state,char,new_state):
		def f2(m,d):
			if m,d == old_state,char:
				return new_state
			else:
				return f(m,d)
	if jsonparse:
		name = ""
		i = 0#curseur
		while i < len(data) and data[i] != '|':
			name += data[i]
			i += 1
		i += 1
		nstate = 0
		while i < len(data) and data[i] != '|':
			nstate = nstate * 10 + data[i]
			i += 1
		states = list(range(data[nstate]))
		def tt(n,ch):
			return Error
		while i < len(data) and data[i] != '|':
			i += 1
	else:
		return Automata(name,states,tt,cs)