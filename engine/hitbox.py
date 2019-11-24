from rect import Rect
from transform import Transform
from vector import Vector
from polygone import Polygon,Line,Segment

DEBUG = False

class Hitbox:
    """ Hit box class """
    def __init__(self,rect):
        self.rect = rect
        self.ctransformable = None

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

    def get_segments(self):
        return self.get_world_poly().get_segments()

    def collide_sides(self,hbox):
        """ Returns sides of this and hbox that collide """
        def compute_index(seglist,poly):
            """ We assume seglist elements are in the same order than in poly.get_segments() - That is the case for the upper function and that's also why I don't want this little function to be accessible elsewhere """
            li = []
            seg = poly.get_segments()
            index_seglist = 0
            for index in range(len(seg)):
                if index_seglist < len(seglist) and seg[index] == seglist[index_seglist]:
                    li.append(index)
                    index_seglist += 1
            return li
        polyf = self.get_world_poly()
        poly2 = hbox.get_world_poly()
        segcf = polyf.segments_collide_with(poly2)
        segc2 = poly2.segments_collide_with(polyf)
        return compute_index(segcf,polyf),compute_index(segc2,poly2)

    def remove_collide(self,hbox):
        epsilon = (1-self.get_ctrbl().rigid_size_factor)/10
        direction = -self.get_ctrbl().get_speed()
        inter_poly = self.get_world_poly().get_intersection(hbox.get_world_poly())
        print(self.get_ctrbl())
        print(direction)
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
    
    def remove_collide2(self,hbox):
        """ Returns the vector that self need to be moved by to remove the collision """
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
