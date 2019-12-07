from controlableNode import ControlableNode
import pygame

class LifeableNode(ControlableNode):
    def __init__(self):
        super().__init__()
        self.max_pv = 5
        self.pv = 3
        self.small = True #small == True -> little health bar over head of the lifeable node

    def set_max_pv(self,v):
        self.max_pv = v
    def set_pv(self,v):
        self.pv = v
    def get_max_pv(self):
        return self.max_pv
    def get_pv(self):
        return self.pv

    def get_percent_life(self):
        return self.get_pv()/self.get_max_pv()

    def aff(self,fen,distorsion,dt):
        print("upper aff",self)
        (px,py,w,h) = self.get_pos_camera(distorsion,self.get_hit_box())
        super().aff(fen,distorsion,dt)
        pygame.draw.rect(fen,(0,0,0),pygame.Rect(px+w/8,py-12,w*0.8,4))
        pygame.draw.rect(fen,(0,255,0),pygame.Rect(px+w/8,py-12,w*self.get_percent_life()*0.8,4))
