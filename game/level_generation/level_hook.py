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

def level_hook(name_of_level, level):
	"""
		Génère un niveau associé au fichier filename
		Renvoie un GameLevel
	"""


	def player_pos_create(speed,tempo):

		def player_pos(t):
			return t*speed*60/tempo*8 #*8 to be faster (but it doesn't match the music anymore !
		return player_pos
	platforms = [SolidPlatform(Hitbox(Rect(i[1],i[2],i[3],i[4]))) for i in level if i[0] == 'p']
	return GameLevel(platforms,player_pos_create(10,60),name=name_of_level)
