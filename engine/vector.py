#!/usr/bin/env python3

import numpy as np

class Vector:
    def __init__(self):
        self.matrix = np.array([[0],[0]])

    def __init__(self,x,y):
        self.matrix = np.array([[x],[y]])

    def homogeneous(self):
        return np.append(self.matrix,[1])

    def x(self):
        return self.matrix[0][0]

    def y(self):
        return self.matrix[0][1]

    def apply_transform(self,transform):
        return transform.transform_vect(self)
