DEBUG = False

import librosa.core, librosa.beat
import numpy as np
import audioread

if(DEBUG):
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

threshold = 0.7

def bpm_info(file):
    """
        Lit le fichier son "file", puis renvoie :
            - le temps en secondes (flottant) du premier beat
            - un tableau des tempos pour chaque beat
            - le nombre total de beats
    """
    y, sr = librosa.core.load(file, sr=None)
    y += np.random.rand(len(y))*0.0001 # Adds noise to the audio input in order to prevent librosa from crashing

    tempo_frames = librosa.beat.tempo(y=y,sr=sr, aggregate=None)
    tempo_times = librosa.times_like(tempo_frames,sr=sr)

    time = 0
    i = 0
    tempos = []
    for i in range(len(tempo_times)):
        if(time <= tempo_times[i]):
            tempos.append(tempo_frames[i])
            time += 60/tempo_frames[i]
    print(tempos,time)

    return (tempo_times[0], tempos, len(tempos))
