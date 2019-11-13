import pygame
import game

class Dialogue_Bubble:

    def __init__(self,msg,talker,background,fen,x,y):
        self.msg = msg
        self.talker = talker
        self.background = background
        self.fen = fen
        self.x = x
        self.y = y

    def show(self,g):
        self.fen.blit(self.background,(self.x,self.y))
        self.fen.blit(self.talker.pic,(self.x,self.y))
        w = self.talker.pic.get_width()
        for i,line in enumerate(self.msg.split("\n")):
            game.T(self.fen,line,self.x+w+10,self.y+i*40+5,size=40,center=False)
        pygame.display.flip()
        cnt = True
        quit_all = False
        while cnt:
            cnt,quit_all = g.dial_loop()
            if quit_all:
                cnt = False
                
        
