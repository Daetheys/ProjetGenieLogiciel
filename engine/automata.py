#!/usr/bin/env python3

from error.exception import TransitionUndefined
from collections import defaultdict
from json import load as jsload


class Automata:
	""" A simple automaton for the SpriteScheduler """
	def __init__(self,name,states,tt,cs,qn):
		self.name = name
		self.states = states
		self.tt = tt#transition table (dictionnary)
		self.cs = cs#current state
		self.qn = qn#map from states to sprites

	def copy(self):
		""" returns a copy of the current automaton """
		return Automata(self.name,self.states,self.tt,self.cs,self.qn)

	def __repr__(self):
		txt = """

		Automaton named %s :

		states 	= %s
		tt 		= %s
		cs 		= %s
		qn 		= %s
		""" % (str(self.name),str(self.states),str(self.tt),str(self.cs),str(self.qn))
		return txt


def create_automaton(data,name=None,states=None,tt=None,cs=None,qn=None,jsonparse=True,nocomment=True):
	"""creates an automaton:
		- from the json parser if jsonparse
		- from the explicitly given data else

	json parser format :  name|n|tt|qn : where
		name(str) is the name
		n	(int) is the number of states
		tt	(str) is of the following format:
			state,char→state; state,char→state ...
			(where 'state' is an int, char is a char)
		qn 	(str) is of the following format:
			state=str,state=str,...
			(where 'state' is an int, str is a str)

	note : tt may be empty. n still has to be followed by |.
	note : the initial state is always set to 0 in a json parser
	note : if nocomment is disabled, str can be of the format: name|n|tt|qn|comments
	"""
	def throwTU(arg=None):
		"""throws the exception TransitionUndefined
		is used in the defaultdict intialization"""
		raise TransitionUndefined(arg)

	def defaultpic():
		""" used in the defaultDict qn """
		return "data/img/default.png"

	def parseint(data,i,marker='|'):
		""" parses an int in a str.
		n : the integer
		i : the position of the first non-integer bit (is marker or len(data))"""
		n = 0
		while i < len(data) and data[i] != marker:
			n = n * 10 + int(data[i])
			i += 1
		return n,i

	def parsestr(data,i,marker='|'):
		""" parses an str in a str.
		n : the obtained string
		i : the position of the first 'marker' bit (is marker or len(data))"""
		n = ''
		while i < len(data) and data[i] != marker:
			n += data[i]
			i += 1
		return n,i

	if jsonparse:
		name = ""
		i = 0#cursor
		while i < len(data) and data[i] != '|':#reading the name
			name += data[i]
			i += 1

		assert data[i] == "|"
		i += 1
		nstate,i = parseint(data,i)#number of states

		assert data[i] == "|"
		states = list(range(nstate))
		tt = defaultdict(throwTU)
		qn = defaultdict(defaultpic)
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
		i += 1#on commence à parser la fonction des états vers les sprites
		while i < len(data) and data[i] != '|':#function from states to sprites

			st,i = parseint(data,i,'=')
			assert data[i] == '='
			i += 1
			qn[st],i = parsestr(data,i,',')#spritename
			assert i >= len(data) or data[i] == ','
			i += 1
		if nocomment: assert i == len(data) or data[i] == '|'
		return Automata(name,states,tt,0,qn)

	else:
		return Automata(name,states,tt,cs,qn)

def create_automaton_hook(dic):
	""" hook for reading automata.json
	creates a full automaton for each automata-like data
	uses heavily the function: create_automaton."""
	for data in dic:
		dic[data] = create_automaton(dic[data])
	return dic

def load_automata():
	"""loads all automata"""
	with open("data/json/automata.json", "r", encoding="utf-8-sig") as read_file:
		dict_ata = jsload(read_file,object_hook=create_automaton_hook)
	return dict_ata

if __name__ != '__main__':
	dict_ata = load_automata()
