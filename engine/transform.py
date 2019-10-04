#!/usr/bin/env python3

import numpy as np
import numpy.linalg as linalg

class Transform:
    def __init__(self, matrix = None):
        if matrix is None:
            self.__matrix = np.identity(3)
        else:
            self.__matrix = matrix
    def get_matrix(self):
        return self.__matrix
    def get_inverse(self):
        try:
            return Transform(linalg.inv(self.__matrix))
        except linalg.LinAlgError:
            return Transform()
    def transformPoint(self,x,y):
        corrected_vector = np.array([[x],[y],[1.]])
        return np.dot(self.__matrix[:2,:],np.array(corrected_vector))
    def transformVect(self,v):
        return self.transformPoint(v[0],v[1])
    def combine(self,t1):
        print(self,'\n',t1)
        self.__matrix = np.dot(self.__matrix,t1.get_matrix())
        print(self,'\n\n')
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
        sX,sY = v,v if type(v) == 'float' else v[0],v[1]
        x,y = center[0],center[1]
        scale_matrix = np.array([ \
                [sX,0,x*(1-sX)], \
                [0,sY,y*(1-sY)],
                [0,0,1]])
        return self.combine(Transform(scale_matrix))
    def __str__(self):
        return str(self.__matrix)


if __name__ == '__main__':
    I = Transform()
    unit = [1,0]
    I.rotate(np.pi/2.)
    print(I.transformVect(unit))
    I.translate([10,10])
    print(I.transformVect(unit))
    I.rotate(-np.pi/2)
    print(I.transformVect(unit))


