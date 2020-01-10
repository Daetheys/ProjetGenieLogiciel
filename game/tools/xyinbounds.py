
def xyinbounds(mx,my,btn):
	""" tests whether (mx,my) is within the bounds of the button btn """
	b1xmin,b1xmax,b1ymin,b1ymax = btn.boundaries()
	return b1xmin <= mx and mx <= b1xmax and b1ymin <= my and my <= b1ymax

