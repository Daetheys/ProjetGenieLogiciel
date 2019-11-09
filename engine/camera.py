import Rect

class Camera:
    def __init__(self):
        self.rect = Rect()

    def is_in_camera(self,polygon):
        """ Returns true if the polygon is completely in the camera's rect or if it intersects a side """
        f_in = True
        for p in polygon.get_points():
            if not(self.rect.contains_vect(p)):
                f_in = False
        (rx,ry) = self.rect.get_position()
        (sx,sy) = self.rect.get_size()
        tl = Vector(rx,ry)
        bl = Vector(rx,ry+sy)
        tr = Vector(rx+sx,ry)
        br = Vector(rx+sx,ry+sy)
        left_seg = Segment(tl,bl)
        top_seg = Segment(tl,tr)
        right_seg = Segment(tr,br)
        bot_seg = Segment(bl,br)
        for side in [left_seg,top_seg,right_seg,bot_seg]:
            f_sides = f_sides and polygon.intersect_segment(side)
        return f_in or f_sides
