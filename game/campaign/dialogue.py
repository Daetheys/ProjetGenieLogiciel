

class Dialogue:
    '''An object that contains a set of Dialogue_Bubble that need to be displayed together (one after the other)'''

    def __init__(self,talk):
        self.talk = talk

    def show(self,g):
        for bubble in self.talk:
            quitall = bubble.show(g)
            if quitall:
                break
        return quitall
