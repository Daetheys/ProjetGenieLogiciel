import pygame

class Parallax():
    """ Scrolling image in the back """
    def __init__(self,name,speed):
        self.name = name
        self.image = None
        self.speed = speed
        self.rect = None
        self.x = 0
        self.fen = None

    def load(self,fen):
        """ Load the pygame image and scales it according to the fen """
        self.fen = fen
        self.image = pygame.image.load(self.name).convert_alpha()
        self.rect = self.image.get_rect()
        fen_height = fen.get_height()
        image_width = max(self.image.get_width(),fen.get_width())
        self.image = pygame.transform.smoothscale(self.image,(image_width,fen_height))
        
    def show(self):
        """ Blit the parallax where it should be (handles the scrolling part"""
        self.fen.blit(self.image,(-self.x,0))
        #self.rect.move_ip(-self.speed,0)
        self.x += self.speed
        if self.x >= self.image.get_width():
            
            self.x = -self.speed*self.image.get_width() #If they are fast they won't be aff too often
