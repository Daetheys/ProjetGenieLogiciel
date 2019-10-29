import librosa.core, librosa.beat

def bpm_info(file):
	"""
		Lit le fichier son "file", puis renvoie :
			- le temps en secondes (flottant) du premier beat
			- le BPM
			- le nombre de beats
	"""
	y, sr = librosa.core.load(file, sr=None)
	tempo, beat_frames = librosa.beat.beat_track(y=y,sr=sr)
	beat_times = librosa.core.frames_to_time(frames=beat_frames,sr=sr)
	return beat_times[0], tempo, len(beat_times)