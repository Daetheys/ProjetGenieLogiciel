import sys
import os

path = os.getcwd()
sys.path.append(path + "/game/level_generation")
sys.path.append(path + "/engine/")

from level_generator import generate_level

def test_gen():
    import pygame
    pygame.init()
    pygame.display.set_mode((1,1))
    generate_level(path + "/data/tests_musique2/120rythmeternaire.mp3")
    pygame.quit()
