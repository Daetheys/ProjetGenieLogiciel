import sys
import os
path = os.getcwd()
sys.path.append(path + "/engine")

from solidPlatform import SolidPlatform
from gameLevel import GameLevel
from player import Player
from rect import Rect
from hitbox import Hitbox
from vector import Vector

import matplotlib as plt

import profile
import pygame

import time

pygame.init()
fen = pygame.display.set_mode((500,500),0)

fen.set_alpha(None)

plat = []
for i in range(100):
    size = 100
    plat.append(SolidPlatform(Hitbox(Rect(-10+i*size,0,size-20,24))))

def pos_player(t):
    return t*200
    
gl = GameLevel(plat,pos_player)

gl.load_camera(fen)
gl.optimise_data()
gl.get_camera().set_dimension(Vector(200,150))

def launch():
    for i in range(1,300):
        gl.play(30)

launch()
