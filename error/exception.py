#Ce fichier contient toutes les exceptions du code (permet de facilement debug)

class WrongSizeMatrix(Exception):
    def __init__(self,arg):
        self.arg = arg
