'''An object that contains a set of Dialogue_Bubble that needs to be displayed together'''

class Dialogue:

    def __init__(self,talk):
        self.talk = talk

    def show(self,g):
        for bubble in self.talk:
            quitall = bubble.show(g)
            if quitall:
                break
        return quitall
