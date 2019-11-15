import pygame
import tools
import buttonMenu


class Dialogue_Bubble:

    def __init__(self,msg,talker,background,x,y,last):
        self.msg = msg
        self.talker = talker
        self.background = background
        self.x = x
        self.y = y
        self.last = last
        
    def display(self,g):
        g.win().blit(self.background,(self.x,self.y))
        g.win().blit(self.talker.pic,(self.x,self.y))
        w = self.talker.pic.get_width()
        for i,line in enumerate(self.msg.split("\n")):
            tools.T(g.win(),line,self.x+w+10,self.y+i*40+5,size=40,center=False)

    def show(self,g):
        h_bg = self.background.get_height()
        b = buttonMenu.ButtonMenu(g,g.options["DISPLAYSIZE_X"]-50,g.options["DISPLAYSIZE_X"]-10,self.y+h_bg-40,self.y+h_bg,g.dict_img["img_cont_dial"],picD=g.dict_img["img_end_dial"],add_to_list=False)
        if self.last:
            b.activation(False)
        else:
            b.activation(True)
        cnt = True
        quit_all = False
        while cnt:
            cnt,quit_all = g.dial_loop(self,blist=[b])
            if quit_all:
                cnt = False


