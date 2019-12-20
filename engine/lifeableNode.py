from controlableNode import ControlableNode
import projectile
import pygame

class LifeableNode(ControlableNode):
    def __init__(self):
        super().__init__()
        self.max_pv = 5
        self.pv = self.max_pv
        self.small = True #small == True -> little health bar over head of the lifeable node

        self.alive = True

    def copy(self):
        l = LifeableNode()
        self.paste_in(l)
        
    def paste_in(self,l):
        super().paste_in(l)
        l.max_pv = self.max_pv
        l.pv = self.pv
        l.small = self.small #Attention ici c'est peut être pas ce qu'on veut
        l.alive = self.alive

    def set_max_pv(self,v):
        self.max_pv = v
    def set_pv(self,v):
        self.pv = v
    def get_max_pv(self):
        return self.max_pv
    def get_pv(self):
        return self.pv

    def get_percent_life(self):
        return max(0,self.get_pv()/self.get_max_pv())

    def take_damages(self,d):
        self.pv -= d
        self.check_alive()
        
    def check_alive(self):
        if self.pv <= 0:
            self.die()

    def die(self):
        self.pv = 0
        self.alive = False

    def aff(self,fen,distorsion,dt):
        font = pygame.font.match_font("ubuntumono",bold=True)
        if self.small:
            (px,py,w,h) = self.get_pos_camera(distorsion,self.get_hit_box())
            super().aff(fen,distorsion,dt)
            pygame.draw.rect(fen,(0,0,0),pygame.Rect(px+w/8,py-12,w*0.8,4))
            length = w*self.get_percent_life()*0.8
            if length:
                pygame.draw.rect(fen,(0,255,0),pygame.Rect(px+w/8,py-12,length,4))
                font = pygame.font.SysFont(font,30,bold=True)
                text = font.render(str(self.get_pv())+"/"+str(self.get_max_pv()), True, (255,255,255))
                rect = text.get_rect()
                rect.topleft = (px+3/4*w,py-12)
                fen.blit(text,rect)
        else:
            super().aff(fen,distorsion,dt)
            w = fen.get_width()
            h = fen.get_height()
            px = int(w*1/12)
            py = int(h*1/8)
            length = w//8
            height = 15
            pygame.draw.rect(fen,(0,0,0),pygame.Rect(px,py,length*0.8,height))
            length = length*self.get_percent_life()*0.8
            if length:
                pygame.draw.rect(fen,(0,255,0),pygame.Rect(px,py,length,height))
                font = pygame.font.SysFont(font,30,bold=True)
                text = font.render(str(self.get_pv())+"/"+str(self.get_max_pv()), True, (255,255,255))
                rect = text.get_rect()
                rect.topleft = (px+3/4*length,py)
                fen.blit(text,rect)

    def collide(self,o2,side,o2_side):
        if isinstance(o2,projectile.Projectile):
            self.take_damages(o2.damages)
