
from pygame import Surface, SRCALPHA
from pygame.image import load
from pygame.transform import smoothscale
from random import randint as randomrandint

def create_plat(width,height,range_p=5):
	""" creates a platform that will appear in the menu """
	plat_img = Surface((width,height), SRCALPHA) # per-pixel alpha
	plat_img.fill((255,255,255,0))
	img = load("data/img/platform3.png").convert_alpha()
	ratio = img.get_height() / height
	smoothscale(plat_img,(int(img.get_width()*ratio),int(img.get_height()*ratio)))
	for i in range(range_p):
		plat_img.blit(img.convert_alpha(),(i*(img.get_width()*ratio-3),0))
	return plat_img

def bgg(l,surf,MAX_X=1800,MAX_Y = 1800,plat_img=None,plat_small=None,plat_big=None):
	""" background generator function
	takes a surface, and blits onto a copied surface some platforms."""
	height = 40
	width = 200
	gap = width + randomrandint(50,width//4)
	if randomrandint(0,1):
		gap += width//2
	speed = max(10,width//20)

	if plat_img is None:
		#Compute platform image
		plat_img = create_plat(width,height,10)

	if plat_big is None:
		plat_big = plat_img
	if plat_small is None:
		plat_small = plat_img

	def blit_list(l,surf):
		for (x,y,z) in l:
			if z == 0:
				surf.blit(plat_img, (x,y))
			elif z == -1:
				surf.blit(plat_small, (x,y))
			elif z == 1:
				surf.blit(plat_big, (x,y))
	L = []
	for i in range(len(l)):#suppression of leftmost platforms
		if l[i][0] > -10 - width:
			L.append((l[i][0] - speed,l[i][1],0))

	#adding platforms to the right
	if L == []:
		size = randomrandint(-1,1)
		L.append((randomrandint(MAX_X-200,MAX_X-150),MAX_Y//2,size))
	elif L[-1][0] < MAX_X:
		size = randomrandint(-1,1)
		L.append(((L[-1][0] + gap + ((gap//2)*size)),L[-1][1] + randomrandint(-height,height),size))
	#print(L)
	surfa = surf.copy()#copies the surface

	#blitting platforms
	blit_list(L,surfa)
	return surfa,L
