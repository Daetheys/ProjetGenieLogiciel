import pygame
import game

class Dialogue_Bubble:

    def __init__(self,msg,talker,background,x,y,last=False):
        self.msg = msg
        self.talker = talker
        self.background = background
        self.x = x
        self.y = y
        self.last = last

    def show(self,g):
        g.win().blit(self.background,(self.x,self.y))
        g.win().blit(self.talker.pic,(self.x,self.y))
        w = self.talker.pic.get_width()
        for i,line in enumerate(self.msg.split("\n")):
            game.T(g.win(),line,self.x+w+10,self.y+i*40+5,size=40,center=False)
        if self.last:
            pass
        pygame.display.flip()
        cnt = True
        quit_all = False
        while cnt:
            cnt,quit_all = g.dial_loop()
            if quit_all:
                cnt = False
                
        
