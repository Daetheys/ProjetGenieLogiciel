"""
Can·A·Baelde v1
-menu is rebuilt with object-oriented programmation
"""
import sys
from os import getcwd
path = getcwd()
path += "/game"#pour import mapDisplayer
sys.path.append(path)
path += "/campaign"#pour import map,etc..
sys.path.append(path)
print(path)

from launcher import Launcher

if __name__ == '__main__':
    g = Launcher()
