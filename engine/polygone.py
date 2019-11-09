import os,sys

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from vector import Vector

class Line:
    """ Represents a line : y = ax+b """
    def __init__(self,a,b,vert=False,x=0):
        self.a = a
        self.b = b
        self.vert = vert
        self.x = x

    def is_point_up(self,p):
        """ Returns true if the point p is in the up side of the line """
        if self.vert:
            return p.x == self.x
        return p.y >= self.a*p.x+self.b

    def intersect_point(self,l2):
        """ Returns the intersect point between two given lines """
        if self.vert:
            return Vector(self.x,l2.a*self.x+l2.b)
        if l2.vert:
            return Vector(l2.x,self.a*l2.x+self.b)
        if self.a-l2.a == 0:
            return None #Parallel lines
        x = (l2.b-self.b)/(self.a-l2.a)
        y = self.a*x+self.b
        return Vector(x,y)

    def __eq__(self,l2):
        if self.vert and l2.vert:
            return self.x and l2.x
        if not(self.vert) and not(l2.vert):
            return self.a == l2.a and self.b == l2.b

    def __repr__(self):
        if self.vert:
            return "Line(vert,"+str(self.x)+")"
        return "Line("+str(self.a)+"x+"+str(self.b)+")"

class Segment:
    """ Represents a segment from vector p1 to vector p2 """
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

    def collide_line(self,l):
        """ Returns true if it collides a specific line """
        b1 = l.is_point_up(self.p1)
        b2 = l.is_point_up(self.p2)
        return b1+b2 == 1

    def collide_segment(self,s):
        ls = s.get_line()
        l = self.get_line()
        inter_p = l.intersect_point(ls)
        print("interp",self,s,inter_p,"\n")
        if inter_p is None: 
            return False #They don't collide
        return self.is_in_interval_x(inter_p.x) and s.is_in_interval_x(inter_p.x)

    def is_in_interval_x(self,x):
        """ Returns if x in the interval of this segment """
        minx = min(self.p1.x,self.p2.x)
        maxx = max(self.p1.x,self.p2.x)
        return minx <= x and x <= maxx
    
    def length(self):
        return ((self.p1.x-self.p2.x)**2+(self.p1.y-self.p2.y)**2)**0.5
        
    def get_line(self):
        if self.p1.x-self.p2.x == 0:
            return Line(0,0,True,self.p1.x)
        a = (self.p1.y-self.p2.y)/(self.p1.x-self.p2.x)
        b = self.p1.y - a*self.p1.x
        return Line(a,b)

    def __eq__(self,s):
        return self.p1 == s.p1 and self.p2 == s.p2

    def __repr__(self):
        return "Segment("+repr(self.p1)+","+repr(self.p2)+")"
        
class Polygon:
    """ Polygon made of a list of vector points"""
    def __init__(self,points):
        self.__points = points
        self.compute_segments()

    def compute_segments(self):
        """ Computes segments from points """
        self.__segments = []
        for i in range(len(self.__points)):
            p1 = self.__points[i%len(self.__points)]
            p2 = self.__points[(i+1)%len(self.__points)]
            self.__segments.append(Segment(p1,p2))

    def get_points(self):
        return self.__points

    def get_segments(self):
        return self.__segments
    
    def translate(self,vector):
        """ Translates the polygon """
        for p in self.__points:
            p.x += vector.x
            p.y += vector.y

    def point_in(self,point):
        """ Returns true if the vector point is in the polygon """
        if point in self.__points:
            return True
        count = 0
        line = Line(0,point.y)
        for i in range(len(self.__points)):
            p1 = self.__points[i%len(self.__points)]
            p2 = self.__points[(i+1)%len(self.__points)]
            if p1.x <= point.x or p2.x <= point.x:
                s = Segment(p1,p2)
                if s.collide_line(line):
                    count += 1
        return count%2 == 1

    def intersect_segment(self,s):
        for si in self.__segments:
            if s.collide_segment(si):
                return True
        return False

    def apply_transform(self,transform):
        li = []
        for p in self.__points:
            v = transform.transform_vect(p)
            li.append(v)
        poly = Polygone(v)
        return poly

    def __repr__(self):
        return "Poly("+str(self.__segments)+")"
