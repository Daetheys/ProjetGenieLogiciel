class DialogueBubble:

    def __init__(self,msg,talker,background,fen,x,y):
        self.msg = msg
        self.talker = talker
        self.background = background
        self.fen = fen
        self.x = x
        self.y = y

    def show(self):
        fen.blit(self.background,(x,y))
