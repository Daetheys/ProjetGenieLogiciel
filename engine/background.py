
class Background():
    def __init__(self,lpar):
        self.lpar = lpar

    def load(self,fen):
        for p in self.lpar:
            p.load(fen)

    def show(self):
        for p in self.lpar:
            p.show()
        
