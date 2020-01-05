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
            - une liste de couples (numéro de beat, BPM jusqu'à ce beat)
            - le nombre de beats
    """
    y, sr = librosa.core.load(file, sr=None)
    y += np.random.rand(len(y))*0.0001 # Adds noise to the audio input in order to prevent librosa from crashing
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr, tempo_min=30, tempo_max=300)

    beat_frames = []
    beat_intensities = []

    for i in range(1,len(pulse)-1):
        if(pulse[i-1] < pulse[i] and pulse[i] > pulse[i+1] and pulse[i] > threshold):
            beat_frames.append(i)
                beat_intensities.append(pulse[i])

    beat_times = librosa.core.frames_to_time(frames=beat_frames,sr=sr)

    tempos = 60/(beat_times[1:]-beat_times[:-1])
    tempo = np.sum(tempos[1:-1])/(len(tempos)-2)

    if(DEBUG):
        print(tempo)
            plt.bar(beat_times,beat_intensities, 0.05)
            plt.plot(beat_times[1:-2],tempos[1:-1])
            plt.show()

    return beat_times[1], [(len(beat_times)-1,tempo)], (len(beat_times)-1)
