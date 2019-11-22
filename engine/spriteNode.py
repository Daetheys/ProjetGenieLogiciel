from node import Node
import pygame
from vector import Vector
from spriteScheduler import SpriteScheduler

class SpriteNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.__state = None #stay,move,damaged,collision,
        self.__sps = None #

    def copy(self):
        sn = SpriteNode()
        self.paste_in(sn)
        return sn

    def paste_in(self,sn):
        Node.paste_in(self,sn)
        sn.set_state(self.get_state())
        if self.get_sps() is not None:
            sn.set_sps(self.get_sps().copy())
        else:
            sn.set_sps(None)

    def set_sps(self,sche):
        self.__sps = sche

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
        scale,trans = distorsion
        transform = box.get_transform()
        world_pos = box.get_self_poly()
        world_rot = transform.cut_translate()
        world_tr = transform.get_translate()
        pos_vect_rot = world_pos.apply_transform(world_rot)
        pos_vect_rot_scal = pos_vect_rot
        pos_vect = pos_vect_rot_scal.apply_transform(world_tr).apply_transform(trans).apply_transform(scale)
        return pos_vect

    def aff(self,fen,distorsion):
        """ Aff this node on the camera"""
        scale,trans = distorsion
        if  self.__sps is not None:
            if self.__sps.loaded:
                img = self.__sps.get_sprite()
            else:
                print("Images should never be imported on-the-fly!")
                exit(0)
                s = self.__sps.get_sprite()
                img = pygame.image.load(s).convert_alpha()
            image_dim = Vector(img.get_width(),img.get_height())
            dist = scale.transform_vect(image_dim)
            x,y = dist.to_tuple()

            img = pygame.transform.smoothscale(img,(int(x),int(y)))
            pos = self.get_position()
            #print("-------1",pos,trans)
            pos = pos.apply_transform(scale)
            pos = pos.apply_transform(trans)
            #print("-------2",pos)
            fen.blit(img,(pos.x ,pos.y ))
        else:
            coll_box = self.get_pos_camera(distorsion,self.get_hit_box())
            rigid_box = self.get_pos_camera(distorsion,self.get_rigid_hit_box())
            pygame.draw.polygon(fen,(0,255,0),coll_box.to_tuples())
            pygame.draw.polygon(fen,(188,0,0),rigid_box.to_tuples())
