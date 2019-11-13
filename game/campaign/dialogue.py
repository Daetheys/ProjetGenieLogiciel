class Dialogue:

    def __init__(self,talk):
        self.talk = talk

    def show(self,g):
        for bubble in self.talk:
            bubble.show(g)