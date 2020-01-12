import pygame
import time
from game.level_generation.level_generator import generate_level
from engine.vector import Vector

pygame.init()
W = 1600
H = 900
FEN = pygame.display.set_mode((W,H))

def visualise(gl):
    pygame.display.flip()
    FEN.set_alpha(None)
    (mini_x,maxi_x,mini_y,maxi_y) = gl.get_size_level()
    mini_x -= abs(mini_x)*1.1
    maxi_x += int(abs(maxi_x)**0.7)
    mini_y -= abs(mini_y)*1.1
    maxi_y += abs(maxi_y)*1.1
    gl.camera.set_position(Vector(mini_x,mini_y))
    dx = maxi_x-mini_x
    dy = maxi_y-mini_y
    gl.camera.set_dimension(Vector(dx,dy))
    #gl.camera.set_position(Vector(-2000,-250))
    #gl.camera.set_dimension(Vector(45000,500))
    gl.load_camera(FEN)
    gl.aff(0.1,gl.objects)
    pygame.draw.rect(FEN,(255,255,255),pygame.Rect(W*5/6,H*5/6,15,50/dy*H))
    pygame.display.flip()
    time.sleep(20)

gl = generate_level("data/musics/cool.mp3")
visualise(gl)
