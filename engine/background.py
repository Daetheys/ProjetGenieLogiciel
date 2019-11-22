
class Background():
    """ List of Parallax """
    def __init__(self,lpar):
        """ lpar is a list of parallax ordered by layer (first -> back) """
        self.lpar = lpar

    def load(self,fen):
        """ Load all parallax """
        for p in self.lpar:
            p.load(fen)

    def show(self):
        """ Show all parallax """
        for p in self.lpar:
            p.show()
        
