from node import Node
import pygame
from vector import Vector
from spriteScheduler import SpriteScheduler

""" It's the evolution of a simple Node : it has a sprite that can be shown on screen. It will need a SpriteScheduler to handle animations (cf SpriteScheduler). """

class SpriteNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.__state = 's' #Represents the actual status of the SpriteNode (it's a letter for it's SpriteScheduler (cf SpriteScheduler)
        self.__sps = None #SpriteScheduler-> if it's None hit boxes will be shown instead of the sprite
        self.animation_speed = 0.05 #Speed of animation (number of frames a single frame stays)
        self.animation_step = 0.0 #Count for the animation

        self.mapping = "Flat" #Way to show the image : Flat : extended // Repeatx : Repeted along x

        self.x_offset = 0
        self.y_offset = 0

    def copy(self):
        """ Returns a copy of this object """
        sn = SpriteNode()
        self.paste_in(sn)
        return sn

    def paste_in(self,sn):
        """ Paste this object in sn """
        Node.paste_in(self,sn)
        sn.set_state(self.get_state())
        if self.get_sps() is not None:
            sn.set_sps(self.get_sps().copy())
        else:
            sn.set_sps(None)

    def stase(self):
        """ Will be called when the object leaves the field of view of the camera -> 0 to remove the object, 1 to keep it """
        return 0

    def set_sps(self,sche):
        self.__sps = sche

    def vanish(self):
        self.create_sps("empty")
        self.set_state("s")

    def unvanish(self,name):
        self.create_sps(name)

    def create_sps(self,name):
        """
        creates the SpriteScheduler associated with the name "name"
        to add/modify such a SpriteScheduler,
        feel free to change the corresponding json.
        """
        sche = SpriteScheduler(name)
        sche.load_automaton()
        sche.load_sprites()
        self.set_sps(sche)

    def get_sps(self):
        """ returns the spriteScheduler associated with the spriteNode"""
        return self.__sps

    def send_char(self,char):
        """ Sends some character of information to the SpriteScheduler """
        self.__sps.step(char)


    def set_state(self,state):
        self.__state = state

    def get_state(self):
        return self.__state

    def get_pos_camera(self,distorsion,box):
        """ Returns the position of a given box in a camera that has a given distorsion (cf Camera) """
        scale,trans = distorsion
        #transform = box.get_transform()
        world_pos = box.get_world_rect()
        #world_rot = transform.cut_translate()
        #world_tr = transform.get_translate()
        #pos_vect_rot = world_pos.apply_transform(world_rot)
        #pos_vect_rot_scal = pos_vect_rot
        #pos_vect = pos_vect_rot_scal.apply_transform(world_tr).apply_transform(trans).apply_transform(scale)
        pos_vect = world_pos.translate2(trans).scale2(scale)
        return pos_vect.get_coord()

    def aff(self,fen,distorsion,dt):
        """ Show this node on the camera"""
        scale,trans = distorsion
        if  self.__sps is not None: #If it's None only hit boxes will be shown
            if self.__sps.loaded: #Check if it's loaded
                if self.animation_step >= self.animation_speed: #Wait for the animation
                    self.__sps.step(self.__state) #Refresh the state/image
                    self.animation_step = 0.0
                self.animation_step += dt
                img = self.__sps.get_sprite() #Get the image associated to the state of its SpriteScheduler
            else:
                #BAD BAD BAD -> the SpriteScheduler should be loaded before using it -> use create_sps(name) instead of set_sps(name)
                print("Images should never be imported on-the-fly!")
                exit(0)
                s = self.__sps.get_sprite()
                img = pygame.image.load(s).convert_alpha()
            #----------------------------------------
            #  Computes where to blit on the camera
            #----------------------------------------
            #Get the box in which this spriteNode needs to be drawn
            (px,py,pw,ph) = self.get_pos_camera(distorsion,self.get_hit_box())
            #Check different types of mapping
            if self.mapping == "Flat":
                #Extends the image
                img = pygame.transform.smoothscale(img,(int(pw),int(ph)))
                fen.blit(img,(int(px)+self.x_offset ,int(py)+self.y_offset ))
            elif self.mapping == "Repeatx":
                #Repeat the image along x axis
                dx = px
                while dx < px+pw and ph != 0:
                    (w,h) = img.get_width(),img.get_height()
                    ratio = (ph/h) #Compute the ratio to fit Y
                    img2 = pygame.transform.smoothscale(img,(int(ratio*w)+1,int(ratio*h))) #Scales the image so that Y will fit
                    fen.blit(img2,(int(dx+0.5)+self.x_offset,int(py)+self.y_offset),(0,0,px+pw-dx,ph))
                    dx += w*ratio #Translates the focus of blit in order to blit a row of sprites (usefull for textures)
            else:
                print("Unknown mapping type. cf SpriteNode.")

        else:
            #Show the hit box because SpriteScheduler is None
            coll_box = self.get_pos_camera(distorsion,self.get_hit_box())
            rigid_box = self.get_pos_camera(distorsion,self.get_rigid_hit_box())
            pygame.draw.rect(fen,(0,255,0),pygame.Rect(*coll_box))
            pygame.draw.rect(fen,(188,0,0),pygame.Rect(*rigid_box))
