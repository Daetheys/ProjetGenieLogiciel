import sys
import os
import numpy as np
import librosa.core, librosa.beat
import glob
import pytest

path = os.getcwd()
sys.path.append(path + "/game/level_generation")

paths = glob.glob(path + "/data/tests_musique2/*.mp3")
paths += glob.glob(path + "/data/tests_musique/*.mp3")
paths += glob.glob(path + "/data/musics/*.mp3")

from sound_parser import bpm_info

def get_sound_duration(filename):
	y, sr = librosa.load(filename, sr=None)
	return librosa.get_duration(y,sr=sr)

def error_margin(x,y):
	return abs((x-y)/y)

def test_tern_tempo():
	(first_beat,tempos,nb_beats) = bpm_info(path + "/data/tests_musique2/120rythmeternaire.mp3")
	(_,tempo) = tempos[0]
	assert(np.round(tempo) == 240)

@pytest.mark.parametrize("filename",paths)
def test_coherence_nb_beats(filename):
	(_,tempos,nb_beats) = bpm_info(filename)
	last_beat_nb = 0
	for (beat_nb,_) in tempos:
		last_beat_nb = beat_nb

	assert last_beat_nb == beat_nb

@pytest.mark.parametrize("filename",paths)
def test_coherence_duration(filename):
	(first_beat,tempos,nb_beats) = bpm_info(filename)
	total_time = first_beat
	last_beat_nb = 0
	for (beat_nb,tempo) in tempos:
		total_time += beat_nb*60/tempo
		last_beat_nb = beat_nb

	assert error_margin(total_time,get_sound_duration(filename)) < 0.05 #Allow a 5% margin error (last beat is not necessarily end of the song)
