from rect import Rect
from transform import Transform
from vector import Vector

class Hitbox:
    """ Hit box class """
    def __init__(self,rect):
        self.rect = rect
        self.ctransformable = None

    """def __repr__(self):
        return "Hitbox("+str(self.rect)+")"
    """

    def center(self):
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
        """ Alias for set_ctrbl """
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
        return self.get_world_poly.to_tuples()

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

    def remove_collide(self,hbox):
        """ Returns the vector that self need to be moved by to remove the collision """
        epsilon = 0.0001
        pf = self.points_in(hbox)
        p2 = hbox.points_in(self)
        if pf + p2 == []:
            return (Vector(0,0),Vector(0,0))
        elif len(pf) >= 1 and p2 == []:
            point = pf[0]
            nwi,d = hbox.rect.nearest_wall(point)
            #print("nwi,d",nwi,d)
            v = hbox.wall_index_to_vector(nwi)*d
            #print("v",v)
            return v.apply_transform(hbox.get_transform().cut_translate())*(1+epsilon)
        elif pf == [] and len(p2) >= 1:
            nwi,d = self.rect.nearest_wall(p2[0])
            #print("nwi,d",nwi,d)
            v = self.wall_index_to_vector(nwi)*d
            #print("v",v)
            return -v.apply_transform(self.get_transform().cut_translate())*(1+epsilon)
        elif len(pf) == 1 and len(p2) == 1:
            nwi,d = self.rect.nearest_wall(p2[0])
            #print("nwi,d",nwi,d)
            v = self.wall_index_to_vector(nwi)*d
            #print("v",v)
            return -v.apply_transform(self.get_transform().cut_translate())*(1+epsilon)
        else:
            print("self",self.get_world_poly())
            print("hbox",hbox.get_world_poly())
            print("pf",pf)
            print("p2",p2)
            assert False #Not handled by physics

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
