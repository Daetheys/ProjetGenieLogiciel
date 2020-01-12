"""
Can·A·Baelde v1.1

"""
import sys
from game.game import Game
import cProfile
import re

if __name__ == '__main__':
    cProfile.run("re.compile(Game())")
    #Game()
    print(sys.path)
