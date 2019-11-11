import sys
import os
import numpy as np

path = os.getcwd()
sys.path.append(path + "/game/level_generation")

from sound_parser import bpm_info

def test_tern():
	(_,tempos,_) = bpm_info(path + "/data/tests_musique2/120rythmeternaire.mp3")
	(_,tempo) = tempos[0]
	assert(np.round(tempo) == 240)