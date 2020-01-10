
from pygame.image import load
from pygame.font import SysFont

def T(cw,txt,x,y,r=0,g=0,b=0,aliasing=1,size=20,center=True):
	"""allows the display of text on screen with or without centering
	the text will be displayed in the window 'cw'
	"""
	font = SysFont(None, size)
	text = font.render(txt, aliasing, (r, g, b))
	if center:
		textpos = text.get_rect(centery=y,centerx=x)
	else:
		textpos = (x,y)
	cw.blit(text, textpos)

