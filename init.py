"""
CanAbaelde v1
-maps are now well displayed
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

g = Launcher()
