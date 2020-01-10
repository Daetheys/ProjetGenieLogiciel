'''
This file is mostly used to create the appropriate dictionaries. 


Here is the format of the json files :

img : {name(str): path(str)}
characters : {name(str): [image(str), color_talk_r(int), color_talk_g(int), color_talk_b(int), inventory]}
dialogue : {name(str): [[name_bubble(str), character(str), image(str), x(int), y(int), is_last(bool)]]}
			= {name(str): [Dialogue_Bubble(list)]}
			= {name(str): talk(list)}
items : {name(str): [type(str), args*]}
'''



import dialogue

def create_dial(dict,dict_str,dict_char,dict_img):
    """ function used to create the dict of dialogues """
    for dial in dict:
        dict[dial] = dialogue.Dialogue(create_bubble(dict[dial],dict_str,dict_char,dict_img))
    return dict

import dialoguebubble

def create_bubble(list,dict_str,dict_char,dict_img):
    """ creates a list of bubble, usable by a DialogueBubble """
    list_bubble = []
    for bubble in list:
        list_bubble.append(dialoguebubble.Dialogue_Bubble(dict_str[bubble[0]],dict_char[bubble[1]],dict_img[bubble[2]],bubble[3],bubble[4],bubble[5]))
    return list_bubble

from pygame.image import load

def create_img(dct):
	""" creates the full dictionnary of pictures in dct. Used with dct_img. """
	for img in dct:
		dct[img] = load(dct[img]).convert_alpha()
	return dct

import character
from collections import defaultdict

def create_char(dict,dict_img):
	""" creates a character from an section of the dictionnary"""
	for char in dict:
		dict[char] = character.Character(char,dict_img[dict[char][0]],(dict[char][1],dict[char][2],dict[char][3]),defaultdict(int))
	return dict

import items

def create_item(dict):
	""" creates an object of a subclass of the class Item """
	for item in dict:
		if dict[item][0] == "key":
			dict[item] = items.KeyItem(item)
		elif dict[item][0] == "pas":
			dict[item] = items.Passive(item,dict[item][1])
		elif dict[item][0] == "csm":
			dict[item] = items.Consommable(item,dict[item][1])
	return dict
