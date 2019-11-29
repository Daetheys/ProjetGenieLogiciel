import buttonMenu
import pygame
from pygame.font import Font

'''An object that can display text with a character'''

class Dialogue_Bubble:

    def __init__(self,msg,talker,background,x,y,last):
        self.msg = msg
        self.talker = talker
        self.background = background
        self.x = x
        self.y = y
        self.last = last
        self.offsetX = 0#the pictures are set that many pixels leftwards
        self.offsetY = 20#the pictures are set that many pixels upwards

    def display(self,g):
        g.win().blit(self.background,(self.x - self.offsetX, self.y - self.offsetY))
        g.win().blit(self.talker.pic,(self.x - self.offsetX, self.y - self.offsetY))
        w = self.talker.pic.get_width()
        x_text,y_text = self.x+w+10,self.y+5
        font = Font(None,40)
        words = [line.split(" ") for line in self.msg.splitlines()]
        space = font.size(' ')[0]
        for line in words:
            for word in line:
                word_surface = font.render(word, 1, (0,0,0))
                word_width,word_height = word_surface.get_size()
                if x_text + word_width >= self.background.get_width():
                    x_text = self.x+w+10  # Reset the x.
                    y_text += word_height  # Start on new row.
                g.win().blit(word_surface, (x_text, y_text))
                x_text += word_width + space
            x_text = self.x+w+10  # Reset the x.
            y_text += word_height  # Start on new row.

    def show(self,g):
        w_bg, h_bg = self.background.get_size()
        b = buttonMenu.ButtonMenu(g,self.x+w_bg-50-self.offsetX,self.x+w_bg-10-self.offsetX,self.y+h_bg-40-self.offsetY,self.y+h_bg-self.offsetY,g.dict_img["img_cont_dial"],picD=g.dict_img["img_end_dial"],add_to_list=False)

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
        return quit_all


