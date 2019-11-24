import os,sys
import numpy as np

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from vector import Vector
from transform import Transform
import random

DEBUG = False

def debug(txt):
    if DEBUG:
        print("DEBUG : ",txt)

class Line:
    """ Represents a line : y = ax+b """
    def __init__(self,a,b,vert=False,x=0):
        self.a = a
        self.b = b
        self.vert = vert
        self.x = x

    def is_point_up(self,p):
        """ Returns true if the point p is in the up side of the line or in the line"""
        if self.vert:
            return p.x == self.x
        return p.y >= self.a*p.x+self.b

    def is_on_line(self,p):
        """ Returns true if the point is in the line """
        if self.vert:
            return np.isclose(p.x,self.x)
        return np.isclose(p.y,self.a*p.x+self.b)

    def contains(self,v):
        return self.is_on_line(v)

    def intersect_point(self,l2):
        """ Returns the intersect point between two given lines """
        if self.vert:
            if l2.vert:
                if self.x == l2.x:
                    return Line(0,0,True,self.x)
                else:
                    return None
            else:
                return Vector(self.x,l2.a*self.x+l2.b)
        if l2.vert:
            return Vector(l2.x,self.a*l2.x+self.b)
        if self.a-l2.a == 0:
            if self.b == l2.b:
                return Line(self.a,self.b) #Superposed lines
            return None #Parallel lines
        x = (l2.b-self.b)/(self.a-l2.a)
        y = self.a*x+self.b
        return Vector(x,y)

    def __eq__(self,l2):
        if self.vert and l2.vert:
            return np.isclose(self.x,l2.x)
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

    def copy(self):
        return Segment(self.p1.copy(),self.p2.copy())

    def collide_line(self,l):
        """ Returns true if it collides a specific line """
        if l.is_on_line(self.p1) or l.is_on_line(self.p2):
            return True
        b1 = int(l.is_point_up(self.p1))
        b2 = int(l.is_point_up(self.p2))
        return (b1+b2) == 1

    def get_inter_line(self,l):
        if self.collide_line(l):
            inter_p = self.get_line().intersect_point(l)
            if isinstance(inter_p,Line):
                return self.copy()
            return inter_p
        else:
            return None    

    def contains(self,v):
        """ Returns True if the vector v is in the segment """
        l = self.get_line()
        return l.is_on_line(v) and self.is_in_interval_x(v.x) and self.is_in_interval_y(v.y)

    def intersect_point(self,s):
        if self.collide_segment(s):
            lf = self.get_line()
            ls = s.get_line()
            ret = lf.intersect_point(ls)
            if isinstance(ret,Line):
                minx = max(self.get_min_x(),s.get_min_x())
                maxx = min(self.get_max_x(),s.get_max_x())
                p1 = Vector(minx,ret.a*minx+ret.b)
                p2 = Vector(maxx,ret.a*maxx+ret.b)
                return Segment(p1,p2)
            return ret
        else:
            return None

    def collide_segment(self,s):
        """ Returns true if both segment intersect """
        def check_side(s1,s2):
            v1 = s1.get_vector()
            s12 = Segment(s1.p2,s2.p1)
            s22 = Segment(s1.p2,s2.p2)
            v12 = s12.get_vector()
            v22 = s22.get_vector()
            return np.sign(v1.cross(v12)) != np.sign(v1.cross(v22))
        std = check_side(self,s) and check_side(s,self)
        rect_hull_inter = not(s.get_max_x() < self.get_min_x() or self.get_max_x() < s.get_min_x() or s.get_max_y() < self.get_min_y() or self.get_max_y() < s.get_min_y())
        col = self.get_vector().cross(s.get_vector()) == 0 and rect_hull_inter
        if DEBUG:
            print(self,s)
            print(check_side(self,s))
            print(check_side(s,self))
            print(std,rect_hull_inter,col)
        return std or col
        

    def get_min_x(self):
        return min(self.p1.x,self.p2.x)

    def get_max_x(self):
        return max(self.p1.x,self.p2.x)

    def get_min_y(self):
        return min(self.p1.y,self.p2.y)

    def get_max_y(self):
        return max(self.p1.y,self.p2.y)

    def is_in_interval_x(self,x):
        """ Returns if x in the interval of this segment """
        minx = self.get_min_x()
        maxx = self.get_max_x()
        return minx <= x and x <= maxx

    def is_in_interval_y(self,y):
        """ Returns if x in the interval of this segment """
        miny = self.get_min_y()
        maxy = self.get_max_y()
        return miny <= y and y <= maxy

    def length(self):
        """ Returns the length of the segment """
        return ((self.p1.x-self.p2.x)**2+(self.p1.y-self.p2.y)**2)**0.5

    def get_line(self):
        """ Returns the line corresponding to the orientation of this segment """
        if self.p1.x-self.p2.x == 0:
            return Line(0,0,True,self.p1.x)
        a = (self.p1.y-self.p2.y)/(self.p1.x-self.p2.x)
        b = self.p1.y - a*self.p1.x
        return Line(a,b)

    def get_vector(self):
        return self.p2+ (-self.p1)

    def __eq__(self,s):
        return self.p1 == s.p1 and self.p2 == s.p2

    def __repr__(self):
        return "Segment("+repr(self.p1)+","+repr(self.p2)+")"

class Polygon:
    """ Polygon made of a list of vector points"""
    def __init__(self,points):
        self.__points = points
        self.compute_segments()
        self.compute_max_min()

    def __truediv__(self,v):
        p2 = self.copy()
        for i in range(len(p2.get_points())):
            p2.__points[i] /= v
        return p2

    def get_mass_center(self):
        p = Vector(0,0)
        for o in self.get_points():
            p += o
        return p/len(self.get_points())
    
    def compute_segments(self):
        """ Computes segments from points """
        self.__segments = []
        for i in range(len(self.get_points())):
            p1 = self.get_points()[i%len(self.get_points())]
            p2 = self.get_points()[(i+1)%len(self.get_points())]
            self.__segments.append(Segment(p1,p2))

    def get_points(self):
        return self.__points

    def get_segments(self):
        return self.__segments

    def translate(self,vector):
        """ Translates the polygon (side effect)"""
        for p in self.get_points():
            p.x += vector.x
            p.y += vector.y

    def translate2(self,vector):
        """ Translates the polygon and returns a new one"""
        poly = self.copy()
        for p in poly.get_points():
            p.x += vector.x
            p.y += vector.y
        return poly

    def rotate(self,angle):
        t = Transform()
        t.rotate(angle)
        p = self.apply_transform(t)
        self.__init__(p.get_points())

    def point_in(self,point):
        if point in self.get_points():
            return True
        sum_angle = 0
        for s in self.get_segments():
            s2 = Segment(point,s.p1)
            s3 = Segment(point,s.p2)
            v2 = s2.get_vector()
            v3 = s3.get_vector()
            sens = np.sign(v2.x*v3.y - v2.y*v3.x)
            if sens == 0 and v2.dot(v3) < 0:
                return True #Point in a segment
            a = s.length()
            b = s2.length()
            c = s3.length()
            val = (-a**2 + b**2 + c**2)/(2*b*c)
            val = max(min(1,val),-1)
            angle = -sens*np.arccos( val )
            sum_angle += angle
        return abs(sum_angle) > np.pi #Is either np.pi*2 or 0 (but with approximation let's cut at np.pi)


    def intersect_segment(self,s):
        """ Returns True if self intersects s """
        for si in self.get_segments():
            if s.collide_segment(si):
                return True
        return False

    def points_in(self,poly):
        """ Returns points of self that are in p """
        l = []
        for p in self.get_points():
            if poly.point_in(p):
                l.append(p)
        return l

    def segments_collide_with(self,poly):
        """ Returns segments of self that are in poly """
        l = []
        for s in self.get_segments():
            if poly.intersect_segment(s):
                l.append(s)
        return l

    def collide(self,poly):
        """ Returns True if the polygon collides with poly """
        if poly.points_in(self) != [] or poly.segments_collide_with(self) != []:
            return True
        return False

    def apply_transform(self,transform):
        """ Apply a transformation on this polygon and returns it"""
        li = []
        for p in self.get_points():
            v = transform.transform_vect(p)
            li.append(v)
        poly = Polygon(li)
        return poly

    def compute_max_min(self):
        """ Compute the rect hull of this polygon (store them inside the object) """
        max_x = None
        min_x = None
        max_y = None
        min_y = None
        for p in self.get_points():
            if max_x is None or p.x > max_x:
                max_x = p.x
            if min_x is None or p.x < min_x:
                min_x = p.x
            if max_y is None or p.y > max_y:
                max_y = p.y
            if min_y is None or p.y < min_y:
                min_y = p.y
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y

    def get_max_x(self):
        return self.max_x

    def get_max_y(self):
        return self.max_y

    def get_min_x(self):
        return self.min_x

    def get_min_y(self):
        return self.min_y

    #Needed for physics 2.0
    #ASSUME this polygon reprensents a Rectangle, may assert False if not


    def get_intersection(self,poly2):
        ptf = self.points_in(poly2)
        pt2 = poly2.points_in(self)
        pt_in = [pt2,ptf]
        l_poly_inter = []
        index = 0
        for s in self.get_segments():
            for ss in poly2.get_segments():
                if s.collide_segment(ss):
                    inter_p = s.intersect_point(ss)
                    if isinstance(inter_p,Vector):
                        if not(inter_p in ptf or inter_p in pt2):
                            l_poly_inter += pt_in[index]+[inter_p]
                            index += 1
                    else:
                        pass
        if l_poly_inter == []: #Un polygon est inclu dans l'autre
            if len(ptf) > len(pt2):
                l_poly_inter = ptf
            else:
                l_poly_inter = pt2
        return Polygon(l_poly_inter)


    def to_rect(self):
        """ Will assert False if the polygon is not a rotated rectangle (angle can be 0). Else it will return the rectangle (posx,posy,width,height),angle """
        if len(self.get_points()) == 4:
            s = self.get_segments()[0]
            l = s.get_line()
            if l.vert:
                angle = np.pi/2
            else:
                angle = np.arctan(l.a)
            p = self.copy()
            p.rotate(angle)
            pts = p.get_points()
            assert np.isclose(pts[0].y,pts[1].y)
            assert np.isclose(pts[1].x,pts[2].x)
            assert np.isclose(pts[2].y,pts[3].y)
            assert np.isclose(pts[3].x,pts[0].x)
            return (pts[0].x,pts[0].y,pts[1].x-pts[0].x,pts[2].y-pts[1].y),angle
        else:
            assert False #Cannot get a rectangle from this polygon

    def copy(self):
        """ Copies this polygon and returns it """
        l = []
        for p in self.get_points():
            l.append(p.copy())
        return Polygon(l)

    def to_tuples(self):
        """ Returns the list of tuples corresponding to this polygon (usefull with pygame) """
        l= []
        for p in self.get_points():
            l.append((p.x,p.y))
        return l

    def __mul__(self,vect):
        l = []
        for p in self.get_points():
            l.append(p.copy()*vect)
        return Polygon(l)

    def __eq__(self,p):
        return self.get_points() == p.get_points()

    def __repr__(self):
        return "Poly("+str(self.get_points())+")"

class Rectangle(Polygon):

    def __init__(self,x,y,l,h):
        """ To create a basic rectangle, the init function is changed.
        It takes the x,y coordinates of the top left corner,
        the length & the height of the Rectangle. It creates then the
        appropriate Vector objects, and initializes itself like a Polygon."""
        a = Vector(x,y)
        b = Vector(x+l,y)
        c = Vector(x+l,y+h)
        d = Vector(x,y+h)
        points = [a,b,c,d]
        Polygon.__init__(self,points)
