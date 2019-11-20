
import sys
import os
#import numpy as np
import pygame
from pygame.locals import *
path = os.getcwd()
path += "/engine"
sys.path.append(path)
path = os.getcwd()
path += "/game/level_generation"
sys.path.append(path)
from level_generator import *
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform,Pattern
from gameLevel import GameLevel
from hypothesis import given
from hypothesis.strategies import integers, lists
from hitbox import Hitbox
from rect import Rect

def level_2_kshan(g):
    """ level 2 """
    gl = generate_level("data/tests_musique2/130accordsmagiques2.mp3")
    #gl = generate_level("data/your music/renegate.mp3")
    gl.load_camera(g.win())#Load the camera in the window fen
    gl.get_camera().set_dimension(Vector(1280,720)) #Resize the camera
    #Usually 2000,2000 (moins de distortion ?) or 2560,1440 (plus grosse résolution)
    gl.get_camera().set_position(Vector(-100,0)) #change pos of  the camera
    gl.aff()

    #execution of the level
    t = 0#time
    fps = g.options["FPS"]# FPS is usually 30
    sec_wait = 3
    while t < g.options["FPS"] * sec_wait:#sec_wait seconds to wait
        pygame.time.Clock().tick(g.options["FPS"])
        #print(t)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False#You failed.
                if event.key == K_RIGHT:
                    print("amaRIGHT")
                if event.key == K_LEFT:
                    print("amaLEFT")
                    x,y = gl.get_camera().get_position().to_tuple()
                    print((x,y))
                    gl.get_camera().set_position(Vector(x-200,y))

        """for pat in RH:
            pat.pattern(t)
            pat.send_char("a")"""

        #Updating the camera
        x,y = gl.get_camera().get_position().to_tuple()
        print((x,y))
        gl.get_camera().set_position(Vector(x+40,y))
        gl.aff()
        g.flip()
        t += 1

    return True#You always succeed. perhaps return a score (integer) ?

