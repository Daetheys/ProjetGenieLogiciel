import pygame

""" A Parallax is a scrolling image in the back of the screen.
It has a speed so that a real background has 0 and the others
must have a transparent part or it will be hard to see the real
background."""

class Parallax():
    """ Scrolling image in the back """
    def __init__(self,image,speed,name=None):
        self.name = name
        self.image = image.convert_alpha() #pygame image
        self.speed = speed #speed (pixels / frame) (Now it is time based... what is it?
        self.rect = None #Size of the image
        self.x = 0 #Offset for the movement
        self.fen = None #Window associated to show it

    def load(self,fen):
        """ Load the pygame image and scales it according to the fen """
        self.fen = fen
        self.rect = self.image.get_rect()
        fen_height = fen.get_height()
        image_width = max(self.image.get_width(),fen.get_width())
        self.image = pygame.transform.smoothscale(self.image,(image_width,fen_height))

    def show(self):
        """ Blit the parallax where it should be (handles the scrolling part"""
        width = self.image.get_width()
        self.fen.blit(self.image,(-self.x,0))
        self.fen.blit(self.image,(width-self.x,0))
        #self.rect.move_ip(-self.speed,0)
        self.x += self.speed
        if self.x >= width: #The image is leaving the screen
            self.x = 0
