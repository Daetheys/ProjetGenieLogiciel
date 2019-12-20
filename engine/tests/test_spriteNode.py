import sys
import os
import numpy as np
import pygame

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from spriteNode import SpriteNode
from rect import Rect
from hitbox import Hitbox
from polygone import Polygon
from vector import Vector

import pygame

pygame.init()
fen = pygame.display.set_mode((500, 500),0)

def test_copy():
    sn = SpriteNode()
    sn.set_state(5)
    sn.set_sps(None)
    sn2 = sn.copy()
    sn.set_state(7)
    assert sn2.get_state() == 5
    assert sn.get_sps() == sn2.get_sps()
    sn.translate(Vector(2,0))
    assert sn2.get_position() == Vector(0,0)
