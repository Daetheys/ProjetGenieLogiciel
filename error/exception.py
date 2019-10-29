#Ce fichier contient toutes les exceptions du code (permet de facilement debug)

class WrongSizeMatrix(Exception):
    def __init__(self,arg=None):
        self.arg = arg

class WrongRectWidth(Exception):
    def __init__(self,arg=None):
        self.arg = arg

class WrongRectHeight(Exception):
    def __init__(self,arg=None):
        self.arg = arg

class TransitionUndefined(Exception):
    def __init__(self,arg=None):
        self.arg = arg
