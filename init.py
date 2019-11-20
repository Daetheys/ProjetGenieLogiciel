"""
Can·A·Baelde v1.1

"""
import sys
from os import getcwd
path = getcwd()
path += "/game"#pour import mapDisplayer
sys.path.append(path)
path += "/campaign"#pour import map,etc..
sys.path.append(path)
path += "/levels/kshan"#pour import level1,etc..
sys.path.append(path)
print(path)

from launcher import Launcher

if __name__ == '__main__':
    Launcher()
