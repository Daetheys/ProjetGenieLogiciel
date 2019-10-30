#!/usr/bin/env python3

from os import getcwd
from sys import path
path0 = getcwd()
path0 += "/error"#works with "/Desktop/ProjetGenieLogiciel/error" for me
path.append(path0)
from exception import TransitionUndefined
from collections import defaultdict
from json import load as jsload

class Automata:
	def __init__(self,name,states,tt,cs):
		self.name = name
		self.states = states
		self.tt = tt#transition table (dictionnary)
		self.cs = cs#current state

def create_automaton(data,name=None,states=None,tt=None,cs=None,jsonparse=True,nocomment=True):
	"""creates an automaton:
		- from the json parser if jsonparse
		- from the explicitly given data else

	json parser format :  name|n|tt : where
		name(str) is the name
		n	(int) is the number of states
		tt	(str) is of the following format:
			state,char→state; state,char→state ...
			(where 'state' is an int, char is a char)

	note : tt may be empty. n still has to be followed by |.
	note : the initial state is always set to 0 in a json parser
	note : if nocomment is disabled, str can be of the format: name|n|tt|comments
	"""
	def throwTU(arg=None):
		"""throws the exception TransitionUndefined
		is used in the defaultdict intialization"""
		raise TransitionUndefined(arg)

	def parseint(data,i,marker='|'):
		""" parses an int in a str.
		n : the integer
		i : the position of the first non-integer bit (is marker or len(data))"""
		n = 0
		while i < len(data) and data[i] != marker:
			n = n * 10 + int(data[i])
			i += 1
		return n,i

	if jsonparse:
		name = ""
		i = 0#cursor
		while i < len(data) and data[i] != '|':#reading the name
			name += data[i]
			i += 1
		#print(name)
		assert data[i] == "|"
		i += 1
		nstate,i = parseint(data,i)#number of states
		#print(nstate)
		assert data[i] == "|"
		states = list(range(nstate))
		tt = defaultdict(throwTU)
		i += 1
		while i < len(data) and data[i] != '|':#adding the transitions

			s,i = parseint(data,i,',')
			assert data[i] == ','
			c = data[i+1]
			assert data[i+2] == '→'
			i += 3
			s2,i = parseint(data,i,';')
			tt[s,c] = s2
			i += 1
		if nocomment: assert i == len(data)
		return Automata(name,states,tt,0)

	else:
		return Automata(name,states,tt,cs)

def create_automaton_hook(dic):
	""" hook for reading automata.json
	creates a full automaton for each automata-like data
	uses heavily the function: create_automaton."""
	for data in dic:
		dic[data] = create_automaton(dic[data])
	return dic

def load_automata():
	"""loads all automata"""
	with open("/home/urem/project/ProjetGenieLogiciel/data/json/automata.json", "r") as read_file:
		dict_ata = jsload(read_file,object_hook=create_automaton_hook)
	return dict_ata

if __name__ != '__main__':
	dict_ata = load_automata()
