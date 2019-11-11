from vector import Vector
from node import Node
from spriteNode import SpriteNode

class MovableNode(SpriteNode):
    """ A node that can move with more powerful functions"""
    def __init__(self):
        super().__init__()
        self.__speed = Vector(0,0)
        self.__acc = Vector(0,0)
        self.__ang_speed = 0
        self.__ang_acc = 0
        self.__force_effect = {}
        self.__mass = 1 #kg
        self.__ang_inertia = 1 #SI

    def set_mass(self,val):
        self.__mass = val
    def get_mass(self):
        return self.__mass
    def set_ang_inertia(self,val):
        self.__ang_inertia = val
    def get_ang_inertia(self):
        return self.__ang_inertia
    def set_acc(self,val):
        self.__acc = val
    def get_acc(self):
        return self.__acc
    def set_ang_acc(self,val):
        self.__ang_acc = val
    def get_ang_acc(self):
        return self.__ang_acc
    def set_speed(self,speed):
        self.__speed = speed
    def get_speed(self):
        return self.__speed
    def set_ang_speed(self,speed):
        self.__ang_speed = speed
    def get_ang_speed(self):
        return self.__ang_speed
    
    def add_force(self,force):
        self.__force_effect[force] = None
    def affected_by_force(self,force):
        try:
            self.__force_effect[force]
            return True
        except KeyError:
            return False
    def list_forces(self):
        return list(self.__force_effect.keys())
    def move(self):
        self.translate(self.get_speed())
        self.rotate(self.get_ang_speed())
    def reverse_move(self):
        self.translate(-self.get_speed())
        self.rotate(-self.get_ang_speed())
    def compute_speed(self,dt):
        #Compute acc
        self.compute_effect_forces()
        #Compute speed
        self.set_speed(self.get_speed() + self.get_acc()*dt)
        self.set_ang_speed(self.get_ang_speed() + self.get_ang_acc()*dt)
    def compute_effect_forces(self):
        forces = self.list_forces()
        acc = Vector(0,0)
        ang_acc = 0
        for f in forces:
            (accf,ang_accf) = f.get_acc(self)
            acc += accf
            ang_acc += ang_accf
        self.set_acc(acc/self.get_mass())
        self.set_ang_acc(ang_acc/self.get_ang_inertia())

    def get_object_collide(self,p):
        """ Returns either the point or the segment that first created a collision between self (moving) and p (not moving) """
        speed = -self.get_speed().copy()
        ang_speed = -self.get_ang_speed()
        factor_max = 1
        factor_min = 0
        timeout = 0
        while 1: #Proceeds by dichotomia assuming last pos wasn't creating a collision but the new one is
            factor = (factor_max+factor_min)/2
            self_cpy = self.get_hit_box().copy()
            assert self_cpy.collide(p)
            self_cpy.translate(speed*factor)
            self_cpy.rotate(ang_speed*factor)
            points_in = p.points_in(self_cpy)
            segments_collide = p.segments_collide_with(self_cpy)
            print("--",factor_max,factor_min)
            print(points_in)
            print(segments_collide)
            if len(points_in) == 1:
                return points_in[0]
            if len(segments_collide) == 1:
                return segments_collide[0]
            if len(points_in) < 1 and len(segments_collide) <1:
                factor_max = factor
            else:
                factor_min = factor
            
            timeout += 1
            if timeout > 10:
                assert False #Timeout in get_object_collide

    def get_segment_collide(self,p):
        obj = self.get_object_collide(p)
        if isinstance(obj,Vector):
            p_points = p.get_points()
            assert len(p_points) > 1 #Rigid bodies can't be reduced to 1 point
            index = p_points.index(obj)
            p1 = p_points[(index-1)%len(p_points)]
            p2 = p_points[(index+1)%len(p_points)]
            s1 = Segment(p1,obj)
            s2 = Segment(obj,p2)
            s1_collide = self.get_hit_box().segments_collide_with(Polygon([s1]))
            s2_collide = self.get_hit_box().segments_collide_with(Polygon([s2]))
            assert s1_collide == s2_collide
            return s1_collide[0]
        else:
            return obj

    def get_resistance_support(self,support):
        seg = self.get_segment_collide(support.get_hit_box())
        (p1,p2) = (seg.p1,seg.p2)
        v = p2 + (-p1)
        v_orth = v.orthogonal()
        return v_orth*self._speed.len()

    def apply_reaction(self,support):
        speed = self.get_resistance_support(support)
        self.set_speed(self.get_speed()+speed)
