import sys
import os
import numpy as np
import copy as copy
import random
import pygame

path = os.getcwd()
sys.path.append(path + "/engine")
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform
from camera import Camera
from gameLevel import GameLevel
from force import Gravity
from hitbox import Hitbox
from rect import Rect
from hypothesis import given
from hypothesis.strategies import integers, lists

pygame.init()
fen = pygame.display.set_mode((500, 500),0)

def test_size_level():
    v1 = Vector(-1,-1)
    v2 = Vector(1,-1)
    v3 = Vector(1,1)
    v4 = Vector(-1,1)
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    Hb2 = Hb.copy()
    plat2 = SolidPlatform(Hb2)
    plat2.translate(Vector(3,2))
    gl = GameLevel([plat1,plat2],[])
    pass
""" #OUTDATED
def test_physics_step1():
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    gravity = Gravity(10)
    plat1.add_force(gravity)
    def pos(t):
        return 0
    gl = GameLevel([plat1],pos)
    gl.physics_step(1)
    assert plat1.get_position() == Vector(0,10)
    assert plat1.get_hit_box().get_world_poly() == Polygon([Vector(-1,9),Vector(1,9),Vector(1,11),Vector(-1,11)])


def test_physics_step2():
    #Check collision with rigid body and gravity
    R = Rect(-1,-1,2,2)
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    
    plat2 = plat1.copy()
    plat2.translate(Vector(0.1,10))
    plat1.rotate(np.pi/4)
    
    gravity = Gravity(10)
    plat1.add_force(gravity)
    
    gl = GameLevel([plat1,plat2],[])
    
    for i in range(7):
        gl.physics_step(0.01)
        
    v = plat2.get_position()
    
    print(v)
    assert v.y < 12
"""

def test_opti():
    R = Rect(0,0,7,2)
    Hb = Hitbox(R)
    plat1 = SolidPlatform(Hb)
    plat = [plat1]
    nb = 10
    for i in range(nb):
        plat.append(plat[-1].copy())
        plat[-1].translate(Vector(10,0))
    gl = GameLevel(plat,[])
    gl.opti_step = 10
    gl.optimise_data()
    for i in range(nb):
        assert len(gl.sorted_objects[i]) == 1
    for x in range(nb*10):
        print("--",x)
        gl.get_camera().set_position(Vector(x/10,0))
        for p in plat:
            if gl.get_camera().is_in_camera(p.get_rigid_hit_box().get_world_rect()):
                print("p",p)
                print("p Hb",p.get_hit_box())
                print("cam",gl.get_camera())
                assert p in gl.get_objects_opti()

def test_physics_high_fall():
    R = Rect(0,0,10,16)
    Hb = Hitbox(R)
    plat = SolidPlatform(Hb)
    def pos(t):
        return 0
    gl = GameLevel([plat],pos)
    gl.player.set_position(0,-100)
    gravity = Gravity(50)
    gl.player.add_force(gravity) #Au cas où la gravité soit nulle dans Gl
    timeout = 1000
    gl.opti_step = 10
    gl.optimise_data()
    while not(gl.player.get_hit_box().collide(plat.get_hit_box())) and timeout > 0:
        print(gl.player.get_hit_box())
        gl.physics_step(0.01,gl.get_objects_opti())
        timeout -= 1
    assert timeout > 0
    assert gl.player.get_position().y <= 0

""" OUTDATED
def test_win_lose_box():
    for (x,y,issue) in [(40,0,True),(2,50,False)]:
        plat = SolidPlatform(Hitbox(Rect(0,0,2,2)))
        plat2 = plat.translate2(Vector(3,3))
        def pos(t):
            return 0
        gl = GameLevel([plat,plat2],pos)
        gl.player.set_position(x,y)
        assert gl.play(30)[0]== issue
"""
