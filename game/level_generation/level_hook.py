DEBUG = False

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

def platform(x,y,xmax):
	"""
		Crée une plateforme de longueur length et de hauteur 12
		ayant son milieu en x,y
		Renvoie un SolidPlatform
	"""
	plat = SolidPlatform(Hitbox(Rect(-abs(xmax-x)//2,12,abs(xmax-x),24)))
	#plat.create_sps("Platform")#voir un sprite
	plat.set_sps(None)#voir une hitbox
	plat.translate(Vector(x,y))
	return plat

def level_hook(filename,name_of_level=''):
	"""
		Génère un niveau associé au fichier filename
		Renvoie un GameLevel
	"""
	with open(filename, "r") as file:
		level = file.read()

	def player_pos(t):
		return t*speed*60/tempo*8 #*8 to be faster (but it doesn't match the music anymore !

	return GameLevel(platforms,player_pos,name=name_of_level)
