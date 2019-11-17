#!/usr/bin/env python3

import numpy as np

class Vector:
    
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vector(-self.x,-self.y)

    def __eq__(self,vect):
        return np.isclose(self.x,vect.x) and np.isclose(self.y,vect.y)

    def __repr__(self):
        return "Vector("+str(self.x)+","+str(self.y)+")"

    def __add__(self,vect):
        return Vector(self.x+vect.x,self.y+vect.y)

    def __mul__(self,val):
        if isinstance(val,Vector):
            return Vector(self.x*val.x,self.y*val.y)
        return Vector(self.x*val,self.y*val)

    def __truediv__(self,val):
        return Vector(self.x/val,self.y/val)

    def orthogonal(self):
        return Vector(self.y,-self.x)

    def normalise(self):
        norm = self.len()
        return Vector(self.x/norm,self.y/norm)

    def cross(self,v):
        return self.x*v.y-self.y*v.x
    
    def dot(self,v):
        return self.x*v.x + self.y*v.y

    def len(self):
        return self.dot(self)**0.5

    def homogeneous(self):
        return np.array([[self.x],[self.y],[1]])

    def apply_transform(self,transform):
        return transform.transform_vect(self)

    def to_list(self):
        return [self.x,self.y]

    def to_array(self):
        return np.array(self.to_list())

    def to_tuple(self):
        return (self.x,self.y)

    def copy(self):
        return Vector(self.x,self.y)
