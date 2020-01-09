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
from flag import Flag

speed_factor = 200

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
    plat = SolidPlatform(Hitbox(Rect(0,0,xmax-x,12)))
    plat.translate(Vector(x,y))
    return plat

def generate_level(filename,name_of_level='',para=True):
        """
            Génère un niveau associé à la musique du fichier filename
            Renvoie un GameLevel
        """
        (first_beat, tempos, nb_beats) = bpm_info(filename)
        print("------",first_beat,tempos,nb_beats)
        platforms = []

        jump_points = [0]
        tempo_index = 0

        for tmp in tempos:
            speed = get_speed(tmp)
            jump_points.append(jump_points[-1]+speed*60/tmp)
        print("generated level length = ", jump_points[-1]/speed, " seconds")

        y = 0#initially the height is at 500 #It's at 0 now ^^
        jump_points[0] = -1000 # Beginning platform

        for i in range(nb_beats):
            #pourquoi +50 et +24 ? #La taille des plateformes non ?
            platforms.append(platform(jump_points[i]+50,y,jump_points[i+1]+24))
            
            dy = random.randint(-24,24)
            y += dy #at each point the y coordinate changes

        def player_pos(t):
            return t*speed

        platforms.append(Flag(Hitbox(Rect(jump_points[-1]+24-20,y-20-dy,10,20))))
        return GameLevel(platforms,player_pos,name=name_of_level,parallax=para)
