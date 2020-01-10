

def insert_score(L,score,name,maxn):
	""" insère score,name dans L, en place et retourne L
	L est une liste leaderboard """
	last = True
	for k in range(len(L)):
		if L[k][1] < score:
			name,L[k][0] = L[k][0],name
			score,L[k][1] = L[k][1],score
			if last:
				L[k][2] = True
				last = False
			else:
				L[k][2] = False
		else:
			L[k][2] = False
	if len(L) < maxn:
		L.append([name,score,last])
	return L
