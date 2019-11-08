class Line:
    """ Represents a line : y = ax+b """
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def is_point_up(self,p):
        """ Returns true if the point p is in the up side of the line """
        return p.y >= a*p.x+b

class Segment:
    """ Represents a segment from vector p1 to vector p2 """
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

    def collide_line(self,l):
        """ Returns true if it collides a specific line """
        b1 = l.is_point_up(p1)
        b2 = l.is_point_up(p2)
        return b1+b2 == 1
        
class Polygon:
    """ Polygon made of a list of vector points"""
    def __init__(self,points):
        self.__points = np.array(points)

    def translate(self,vector):
        """ Translates the polygon """
        for p in self.points:
            p.x += vector.x
            p.y += vector.y

    def point_in(self,point):
        """ Returns true if the vector point is in the polygon """
        count = 0
        line = Line(0,point.y)
        for i in range(len(self.points)-1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            if p1.x <= point.x or p2.x <= point.x:
                s = Segment(p1,p2)
                if s.collide_line(line):
                    count += 1
        return count%2 == 0
