DEBUG = False

import random

from sound_parser import bpm_info

import sys
import os

path = os.getcwd()
sys.path.append(path + "/engine")

from vector import Vector
from polygone import Polygon
from gameLevel import GameLevel
from solidPlatform import SolidPlatform

speed_factor = 350

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
	p = Polygon([
			Vector(0,0),
			Vector(xmax-x,0),
			Vector(xmax-x,24),
			Vector(0,24)
		])
	plat = SolidPlatform(p)
	plat.translate(Vector(x,y))
	return plat

def generate_level(filename):
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


	y = 0
	jump_points[0] = -10000
	
	for i in range(nb_beats):
		platforms.append(platform(jump_points[i]+50,y,jump_points[i+1]+24))

		y += random.randint(-48,48)

	return GameLevel(platforms,[])