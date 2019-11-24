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

""" Transform objects represents a transformation made by a matrix on 2D objects. It needs to be able to compute translations, rotations and scalling to apply them to transformables (and hit boxes). A transform object represents a 3x3 matrix made of a 2x2 upper left part for rotation and scaling and the last column for translations. They can be combined (and that's where we'll need other coefficients) to make more complex transformations """

debug = True

class Transform:
    """ Represents a matrix to transform transformables (vectors) """

    def __init__(self, matrix = None):
        """ If nothing is given, it's the identity """
        if matrix is None: #It starts with identity if nothing given as parameter -> it will then be translated, rotated or scaled
            self.matrix = np.identity(3)
        elif matrix.shape == (3,3): #The matrix must be 3x3
            self.matrix = matrix
        else:
           raise WrongSizeMatrix(matrix)

    def copy(self):
        """ Returns a copy of this object (unlinked) """
        tr = Transform()
        tr.matrix = self.matrix.copy()
        return tr

    def __repr__(self):
        """ To print it """
        return str(self.matrix)

    def __eq__(self,tr):
        """ Using an approximation here """
        return np.allclose(self.matrix,tr.matrix)

    def cut_translate(self):
        """ Returns the transform without translation """
        mat = self.matrix.copy()
        mat[:,2] = np.array([0,0,0])
        mat[2,:] = np.array([0,0,0])
        mat[2,2] = 1
        return Transform(mat)

    def get_translate(self):
        """ Returns only the translation of this """
        mat = self.matrix.copy()
        mat[:,:2] = np.array([[1,0],[0,1],[0,0]])
        return Transform(mat)
    
    def get_matrix(self):
        """ Returns the matrix """
        return self.matrix

    def get_inverse(self):
        """ Returns the inverse matrix """
        try:
            return Transform(linalg.inv(self.matrix))
        except linalg.LinAlgError:
            if debug:
                print("Carefull : Linalg Error, a transform got identity instead of inverse\n")
            return Transform()

    def transform_point(self,x,y):
        """ Transforms a point x,y """
        return self.transform_vect(Vector(x,y))

    def transform_vect(self,v):
        """ Transforms a vector /!\ Returns a np.array """
        arr = np.dot(self.matrix[:2,:],v.homogeneous())
        return Vector(arr[0][0],arr[1][0])

    def combine(self,t1):
        """ Dot with an other transform -> right side """
        self.matrix = np.dot(t1.get_matrix(),self.matrix)
        return self

    def translate(self,v):
        """ Translates the matrix """
        translation_matrix = np.array([\
                [1,0,v.x], \
                [0,1,v.y], \
                [0,0,1]])
        return self.combine(Transform(translation_matrix))
    
    def rotate(self,angle):
        """ Rotates the matrix """
        cos = np.cos(angle)
        sin = np.sin(angle)
        rotation_matrix = np.array([ \
                [cos,-sin,0], \
                [sin, cos,0], \
                [0,0,1]])
        return self.combine(Transform(rotation_matrix))

    def scale(self,v):
        """ Scales the matrix """
        sX,sY = (v,v) if isinstance(v,float) else (v.x,v.y)
        scale_matrix = np.array([\
                [sX,0,0],\
                [0,sY,0],\
                [0,0,1]])
        return self.combine(Transform(scale_matrix))
