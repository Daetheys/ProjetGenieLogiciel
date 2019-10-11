#!/usr/bin/env python3

import numpy as np
import numpy.linalg as linalg
import os
import sys
path = os.getcwd()
path = path[:-7]
sys.path.append("error")
sys.path.append(path)
from exception import WrongSizeMatrix

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
        
    def transformPoint(self,x,y):
        corrected_vector = np.array([[x],[y],[1.]])
        reducted_matrix = self.matrix[:2,:]
        return np.dot(self.matrix[:2,:],np.array(corrected_vector))
    
    def transformVect(self,v):
        return self.transformPoint(v[0],v[1])
    
    def combine(self,t1):
        self.matrix = np.dot(self.matrix,t1.get_matrix())
        return self
    
    def translate(self,v):
        x,y = v[0],v[1]
        translation_matrix = np.array([\
                [1,0,x], \
                [0,1,y], \
                [0,0,1]])
        return self.combine(Transform(translation_matrix))
    def rotate(self,angle):
        cos = np.cos(angle)
        sin = np.sin(angle)
        rotation_matrix = np.array([ \
                [cos,-sin,0], \
                [sin, cos,0], \
                [0,0,1]])
        print('rotation matrix :\n', rotation_matrix)
        return self.combine(Transform(rotation_matrix))
    def rotate_around(self,angle,center):
        x,y = center[0],center[1]
        cos = np.cos(angle)
        sin = np.sin(angle)
        rotation_matrix = np.array([\
                [cos,-sin,x*(1-cos) + y*sin], \
                [sin, cos,y*(1-cos) - x*sin], \
                [0,0,1]])
        return self.combine(Transform(rotation_matrix))
    def scale(self,v):
        sX,sY = (v,v) if isinstance(v, float) else (v[0],v[1])
        scale_matrix = np.array([[sX,0,0],[0,sY,0],[0,0,1]])
        return self.combine(Transform(scale_matrix))
    def scale_around(self,v,center):
        sX,sY = (v,v) if type(v) == 'float' else (v[0],v[1])
        x,y = center[0],center[1]
        scale_matrix = np.array([ \
                [sX,0,x*(1-sX)], \
                [0,sY,y*(1-sY)],
                [0,0,1]])
        return self.combine(Transform(scale_matrix))
    def __str__(self):
        return str(self.matrix) + '\n'


if __name__ == '__main__':
    I = Transform()
    unit = [0,0]
    I.rotate(np.pi/2.)
    print('matrix :\n',I,'\n',I.transformVect(unit),'\n\n')
    I.translate([10,10])
    print('matrix :\n',I,'\n',I.transformVect(unit),'\n\n')
    I.rotate(-np.pi/2.)
    print('matrix :\n',I,'\n',I.transformVect(unit),'\n\n')
    I.rotate(-np.pi/2.)
    print('matrix :\n',I,'\n',I.transformVect(unit),'\n\n')


