DEBUG = False

import random

from game.level_generation.sound_parser import bpm_info

import sys
import os

from engine.vector import Vector
from engine.polygone import Polygon
from engine.gameLevel import GameLevel
from engine.solidPlatform import SolidPlatform
from engine.hitbox import Hitbox
from engine.rect import Rect

from engine.flag import Flag
from engine.pickableNode import Coin

random.seed(0)
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

def add_coins(objects,x0,y0,width,height,number):
    for i in range(number):
        if(number > 1):
            coeff = i/(number-1)
        else:
            coeff = 0.5
        #objects.append(Coin(Hitbox(Rect(x0,y0,10,10))))
        objects.append(Coin(Hitbox(Rect(x0+coeff*width,y0+coeff*height,10,10))))

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

        objects = []

        objects.append(Flag(Hitbox(Rect(jump_points[-1]+24-10,y-20-dy,10,20)))) # Add flag

        for i in range(len(platforms)):
            rd = random.random()
            if(rd < 0.25):
                (x,y,w,h) = platforms[i].get_hit_box().get_world_rect().get_coord()
                w -= 10
                nb = 3
                if(rd < 0.10):
                    nb = 5
                add_coins(objects,x+w/3,y-h,w/3,0,nb)

        for i in range(len(platforms)-1):
            rd = random.random()
            if(rd < 0.33):
                (x1,y1,w1,h1) = platforms[i].get_hit_box().get_world_rect().get_coord()
                (x2,y2,w2,h2) = platforms[i+1].get_hit_box().get_world_rect().get_coord()
                w1 -= 10
                w2 -= 10
                start_x = x1+w1
                end_x = x2
                start_y = y1-45
                end_y = y2-45
                add_coins(objects, start_x, start_y, end_x - start_x, end_y - start_y, random.randint(2,3))

        print(platforms+objects)

        return GameLevel(platforms+objects,player_pos,name=name_of_level,parallax=para)
