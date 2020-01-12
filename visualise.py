import pygame
import time
from game.level_generation.level_generator import generate_level
from engine.vector import Vector
from argparse import ArgumentParser

pygame.init()
i = pygame.display.Info()
W = int( i.current_w * 9/10 )
H = int( i.current_h * 9/10 )
FEN = pygame.display.set_mode((W,H))

def visualise(filepath="data/your music/"):
	"""a Visualiser for music generated level, as required for part 2.
	
	The white rectangle is the maximal jump height."""

	parser = ArgumentParser()
	parser.add_argument("filename",
						help="name of the file you want to see.",
						type=str, default="cool.wav", nargs='?')
	name = parser.parse_args().filename
	print("File chosen : "+name)
	filepath += name
	gl = generate_level(filepath)
	pygame.display.flip()
	FEN.set_alpha(None)
	(mini_x,maxi_x,mini_y,maxi_y) = gl.get_size_level()
	mini_x -= int(abs(mini_x)*1.1)
	maxi_x += int(abs(maxi_x)**0.7)
	mini_y -= int(abs(mini_y)*1.1)
	maxi_y += int(abs(maxi_y)*1.1)
	gl.camera.set_position(Vector(mini_x,mini_y))
	dx = maxi_x-mini_x
	dy = maxi_y-mini_y
	gl.camera.set_dimension(Vector(dx,dy))
	gl.load_camera(FEN)
	gl.aff(0.1,gl.objects)
	pygame.draw.rect(FEN,(255,255,255),pygame.Rect(W*5/6,H*5/6,15,50/dy*H))
	pygame.display.flip()
	time.sleep(20)

visualise()
