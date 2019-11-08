import sys
import os
import numpy as np

path = os.getcwd()
music_path = path + "/data/musique/test_musique2/120rythmeternaire.mp3"
path += "/game/level_generation"
sys.path.append(path + "/game/level_generation")
sys.path.append(path + "/data/musique/test_musique")
sys.path.append(path + "/data/musique/test_musique2")

from sound_parser import bpm_info


(_,tempo,_) = bpm_info("120rythmeternaire.mp3")
assert(np.round(tempo) == 240)