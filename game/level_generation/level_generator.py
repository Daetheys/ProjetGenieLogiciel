DEBUG = False

import random

from sound_parser import bpm_info

import sys
import os

path = os.getcwd()
sys.path.append(path + "/engine")
sys.path.append(path + "/game")

from vector import Vector
from polygone import Polygon
from gameLevel import GameLevel
from solidPlatform import SolidPlatform
from hitbox import Hitbox
from rect import Rect

speed_factor = 1000

def get_speed(tempo):
	"""
		Renvoie la vitesse (en unités spatiales par seconde) en fonction du tempo
	"""
	return speed_factor


def platform(x,y,xmax):
	"""
		Crée une plateforme de longueur length et de hauteur 12 ayant son coin
		supérieur gauche aux coordonnées x,y
		Renvoie un SolidPlatform
	"""
	""" Ancien code écrit par Elies
	p = Polygon([
			Vector(0,0),
			Vector(xmax-x,0),
			Vector(xmax-x,24),
			Vector(0,24)
		])
	plat = SolidPlatform(p)
	"""
	plat = SolidPlatform(Hitbox(Rect(-abs(xmax-x)//2,12,abs(xmax-x),24)))
	#plat.create_sps("Platform")#voir un sprite
	plat.set_sps(None)#voir une hitbox
	plat.translate(Vector(x,y))
	return plat

def generate_level(filename,name_of_level=''):
	"""
		Génère un niveau associé à la musique du fichier filename
		Renvoie un GameLevel
	"""
	(first_beat, tempos, nb_beats) = bpm_info(filename)

	platforms = []

	jump_points = [0]
	tempo_index = 0
	for i in range(nb_beats):
		(last_beat, tempo) = tempos[tempo_index]
		speed = get_speed(tempo)

		jump_points.append(jump_points[i]+speed*60/tempo)

		if(i > last_beat):
			tempo_index = tempo_index + 1

	y = 0#initially the height is at 500 #It's at 0 now ^^
	#jump_points[0] = 0 #avec -10 000 ça ne marche pas, je ne sais pas pourquoi!

	for i in range(nb_beats):
		#pourquoi +50 et +24 ? #La taille des plateformes non ?
		platforms.append(platform(jump_points[i]+50,y,jump_points[i+1]+24))

		y += random.randint(-48,48)#at each point the y coordinate changes

	def player_pos(t):
		return t*speed*60/tempo*8 #*8 to be faster (but it doesn't match the music anymore !


	return GameLevel(platforms,player_pos,name=name_of_level)
