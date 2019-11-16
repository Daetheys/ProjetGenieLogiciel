import sys
import os

path = os.getcwd()
sys.path.append(path + "/game/level_generation")
sys.path.append(path + "/engine/")

from level_generator import generate_level

def test_gen():
	generate_level(path + "/data/tests_musique2/120rythmeternaire.mp3")
