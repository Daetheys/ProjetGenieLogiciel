#!/usr/bin/env python3

import numpy as np
import numpy.linalg as linalg
import os
import sys
path = os.getcwd()
path += "/error"
sys.path.append(path)
from exception import WrongSizeMatrix

from vector import Vector

debug = True

class Transform:

    def __init__(self, matrix = None):
        if matrix is None:
            self.matrix = np.identity(3)
        elif matrix.shape == (3,3):
            self.matrix = matrix
        #else:
           #raise WrongSizeMatrix(matrix)

    def get_matrix(self):
        return self.matrix

    def get_inverse(self):
        try:
            return Transform(linalg.inv(self.matrix))
        except linalg.LinAlgError:
            if debug:
                print("Carefull : Linalg Error, a transform got identity instead of inverse\n")
            return Transform()

    def transform_point(self,x,y):
        return self.transform_vect(Vector(x,y))

    def transform_vect(self,v):
        return np.dot(self.matrix[:2,:],v.homogeneous())

    def combine(self,t1):
        self.matrix = np.dot(self.matrix,t1.get_matrix())
        return self

    def translate(self,v):
        translation_matrix = np.array([\
                [1,0,v.x], \
                [0,1,v.y], \
                [0,0,1]])
        return self.combine(Transform(translation_matrix))
    
    def rotate(self,angle):
        angle *= -1
        cos = np.cos(angle)
        sin = np.sin(angle)
        rotation_matrix = np.array([ \
                [cos,-sin,0], \
                [sin, cos,0], \
                [0,0,1]])
        return self.combine(Transform(rotation_matrix))
    
    def rotate_around(self,angle,center):
        #I don't know what this does -> not tested
        angle *= -1
        x,y = center.x,center.y
        cos = np.cos(angle)
        sin = np.sin(angle)
        rotation_matrix = np.array([\
                [cos,-sin,x*(1-cos) + y*sin], \
                [sin, cos,y*(1-cos) - x*sin], \
                [0,0,1]])
        return self.combine(Transform(rotation_matrix))
    
    def scale(self,v):
        sX,sY = (v,v) if isinstance(v,float) else (v.x,v.y)
        scale_matrix = np.array([\
                [sX,0,0],\
                [0,sY,0],\
                [0,0,1]])
        return self.combine(Transform(scale_matrix))
    
    def scale_around(self,v,center):
        #I don't know what that does -> not tested
        sX,sY = (v,v) if isinstance(v,float) else (v.x,v.y)
        x,y = center.x,center.y
        scale_matrix = np.array([ \
                [sX,0,x*(1-sX)], \
                [0,sY,y*(1-sY)],
                [0,0,1]])
        return self.combine(Transform(scale_matrix))
    def __str__(self):
        return str(self.matrix) + '\n'
