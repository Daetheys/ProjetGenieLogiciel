from rect import Rect
from transform import Transform
from vector import Vector
from polygone import Polygon,Line,Segment

DEBUG = False

""" Fondamentally a hit box is a rect that has a link to a transformable. It uses its get_transform to compute collisions in its referential or in the real world """

class Hitbox:
    """ Hit box class """
    def __init__(self,rect):
        self.rect = rect #Rect
        self.ctransformable = None #CollideTransformable

    def __repr__(self):
        return "Hitbox("+str(self.get_world_poly())+")"
    
    def get_rect(self):
        return self.rect
    
    def center(self):
        """ Centers the rectangle on (0,0) """
        return self.rect.center()

    def copy(self):
        """ UNLINKED COPY """
        hb = Hitbox(self.rect.copy())
        return hb

    def rescale(self,alpha):
        self.rect.rescale(alpha)

    def get_ctrbl(self):
        """ Get collide transformable associated with this hit box """
        return self.ctransformable

    def set_ctrbl(self,ct):
        """ Set it """
        self.ctransformable = ct

    def link(self,ct):
        """ Alias for set_ctrbl -> easier to remember"""
        self.set_ctrbl(ct)
        
    def get_transform(self):
        """ Return the transform of this hit box """
        return self.ctransformable.get_transform()

    def get_inv_transform(self):
        """ Idem with inv transform """
        return self.ctransformable.get_inverse_transform()

    def get_self_poly(self):
        """ Returns the polygon in the self space (self referential space) """
        return self.rect.get_poly()

    def get_world_poly(self):
        """ Returns the polygon in the world space (level referential space) """
        return self.rect.get_poly().apply_transform(self.get_transform())

    def get_other_poly(self,hbox):
        """ Returns the polygon in an other space (other referential space) given a transform matrix """
        return self.get_world_poly().apply_transform(hbox.get_inv_transform())

    def to_tuples(self):
        return self.get_world_poly().to_tuples()

    def points_in(self,hbox):
        """ Returns points from self that are in hbox, in the referential of hbox """
        poly = self.get_other_poly(hbox)
        l = []
        for p in poly.get_points():
            if hbox.rect.point_in(p):
                l.append(p)
        return l

    def collide(self,hbox):
        """ Returns true if both hit box collide """
        return bool(self.points_in(hbox) + hbox.points_in(self))

    def get_segments(self):
        return self.get_world_poly().get_segments()

    def collide_sides(self,hbox):
        """ Returns sides of this and hbox that collide """
        polyf = self.get_world_poly()
        poly2 = hbox.get_world_poly()
        #Computes the intersection polygon
        inter_poly = polyf.get_intersection(poly2)
        #It will now be separed in 2 different parts : the one from polyf and the one from poly2. To estimate where the collision has happened this function will return the index of the longest segment for each of those parts. This index is 0 for the top, 1 for right, 2 for bottom and 3 for left.
        lenf = 0 #Max length for segments of the part of polyf
        indexf = None #Associated index
        len2 = 0 #Max length for segments of the part of poly2
        index2 = None #Associated index
        if DEBUG:
            print("self",self.get_world_poly())
            print("hbox",hbox.get_world_poly())
            print("inter poly",inter_poly)
        #Check whether s is in polyf or in poly2 and checks with lenf and len2 to compute indexf and index2
        for s in inter_poly.get_segments():
            if DEBUG:
                print("--s",s)
            #Check in polyf if s is in it
            for i,sf in enumerate(polyf.get_segments()):
                inter_p = sf.intersect_point(s)
                if DEBUG:
                    print("i",i)
                    print("sf",sf)
                    print("inter_p",inter_p)
                if isinstance(inter_p,Segment): #If the intersection is a segment, s is included in sf
                    length = s.length()
                    if length >= lenf: #Check whether its length is high enough to be kept
                        if DEBUG:
                            print("OKf",length,lenf)
                        lenf = length
                        indexf = i
            if DEBUG:
                print("--")
            #Check in poly2 if s is in it
            for i,s2 in enumerate(poly2.get_segments()):
                inter_p = s2.intersect_point(s)
                if DEBUG:
                    print("i",i)
                    print("s2",s2)
                    print("inter_p",inter_p)
                if isinstance(inter_p,Segment): #If the intersection is a segment, s is included in s2
                    length = s.length()
                    if length >= len2: #Check whether its length is high enough to be kept
                        if DEBUG:
                            print("OK")
                        len2 = length
                        index2 = i
        return indexf,index2

    def remove_collide(self,hbox):
        """ removes the collision with hbox using the speed of self.get_ctrbl() """
        epsilon = (1-self.get_ctrbl().rigid_size_factor)/10
        direction = -self.get_ctrbl().get_speed()
        inter_poly = self.get_world_poly().get_intersection(hbox.get_world_poly())
        #print(self.get_ctrbl())
        #print(direction)
        if DEBUG:
            print("remove_collide")
            print("self rigid box",self.get_world_poly())
            print("hbox rigid box",hbox.get_world_poly())
            print("inter_poly",inter_poly)
        lenmax = 0
        for p in inter_poly.get_points():
            if direction.x == 0:
                l = Line(0,0,True,p.x)
            else:
                a = direction.y/direction.x
                l = Line(a,p.y-a*p.x)
            if DEBUG:
                print("p",p)
                print("line",l)
            for s in inter_poly.get_segments():
                inter_p = s.get_inter_line(l)
                if DEBUG:
                    print("s",s)
                    print("inter_p",inter_p)
                if inter_p is None:
                    pass
                elif isinstance(inter_p,Segment):
                    length = inter_p.length()
                    if DEBUG:
                        print("length",length)
                    if length > lenmax:
                        lenmax = length
                else:
                    length = Segment(inter_p,p).length()
                    if DEBUG:
                        print("length",length)
                    if length > lenmax:
                        lenmax = length
        return direction.normalise()*(lenmax*(1+epsilon))

    """ Physics 2.0 (it took me so much time to o it I don't want to delete it) -> changed because it doesn't work that well
    def remove_collide2(self,hbox):
        # Returns the vector that self need to be moved by to remove the collision (used on rigid body collide boxes)
        epsilon = 0.0001
        pf = self.points_in(hbox)
        p2 = hbox.points_in(self)
        if pf + p2 == []: #Shouldn't happen if use when a rigid collision occurs
            return Vector(0,0) #there is no collision
        elif len(pf) >= 1 and p2 == []:
            point = pf[0]
            nwi,d = hbox.rect.nearest_wall(point)
            v = hbox.wall_index_to_vector(nwi)*d
            return v.apply_transform(hbox.get_transform().cut_translate())*(1+epsilon)
        elif pf == [] and len(p2) >= 1:
            nwi,d = self.rect.nearest_wall(p2[0])
            v = self.wall_index_to_vector(nwi)*d
            return -v.apply_transform(self.get_transform().cut_translate())*(1+epsilon)
        elif len(pf) == 1 and len(p2) == 1:
            nwi,d = self.rect.nearest_wall(p2[0])
            v = self.wall_index_to_vector(nwi)*d
            return -v.apply_transform(self.get_transform().cut_translate())*(1+epsilon)
        else:
            print("self",self.get_world_poly())
            print("hbox",hbox.get_world_poly())
            print("pf",pf)
            print("p2",p2)
            assert False #Not handled by physics
        """
    def wall_index_to_vector(self,index):
        if index == 0:
            return Vector(-1,0)
        elif index == 1:
            return Vector(0,-1)
        elif index == 2:
            return Vector(1,0)
        elif index == 3:
            return Vector(0,1)
        else:
            assert False #Wrong index in Rect.wall_index_to_vector
