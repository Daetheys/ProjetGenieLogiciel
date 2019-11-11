import pygame

class Dialogue_Bubble:

    def __init__(self,msg,talker,background,fen,x,y):
        self.msg = msg
        self.talker = talker
        self.background = background
        self.fen = fen
        self.x = x
        self.y = y

    def show(self):
        cnt = False
        self.fen.blit(self.background,(x,y))
        self.fen.blit(self.talker.pic,(x,y))
        T(fen,msg,x,y)
        while not cnt:
            for event in pygame.event.get():
                if event.key == K_SPACE:
                    cnt = True
                
        
