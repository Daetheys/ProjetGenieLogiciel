#!/usr/bin/env python3

import numpy as np

class Vector:
    
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __eq__(self,vect):
        return np.isclose(self.x,vect.x) and np.isclose(self.y,vect.y)

    def __repr__(self):
        return "Vector("+str(self.x)+","+str(self.y)+")"

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
