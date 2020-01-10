
def score_to_msg(leaderboard):
	""" Creates the message that will be printed in the leaderboard """
	msg="LEADERBOARD\n\n"
	for i,score in enumerate(leaderboard):
		if score[2]:
			msg += str(i+1) + ") " + score[0] + " : " + str(score[1]) + "    *\n"
		else:
			msg += str(i+1) + ") " + score[0] + " : " + str(score[1]) + "\n"
	return msg

def inv_to_msg(inv):
	""" Creates the message that will be printed in the inventory """
	msg="INVENTORY\n\n"
	for item in inv:
		if inv[item] > 0:
			add = item.name
			if inv[item] > 1:
				add += " : " + str(inv[item])
			add += "\n"
			msg += add
	return msg

from collections import defaultdict

def list_to_defaultdict(li):
	""" transforms a list of pair into a defauldict """
	d = defaultdict(int)
	for tup in li:
		d[tup[0]] = tup[1]
	return d

