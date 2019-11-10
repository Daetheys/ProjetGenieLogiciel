from camera import Camera
from vector import Vector

class GameLevel:
    """ Level of the game """
    def __init__(self,objects):
        """ The player spawn in (0,0) """
        self.camera = Camera()
        self.camera.set_position(Vector(0,0))
        self.camera.set_dimension(Vector(10,5))
        self.objects = objects
        self.compute_size_level()
        self.physics_resolution = 1
        self.data_collision_objects = {}
        self.compute_data_collision_objects()

    def get_camera(self):
        return self.camera

    def compute_size_level(self):
        """ Computes the size of the level """
        maxi_x = 0
        maxi_y = 0
        mini_x = 0
        mini_y = 0
        #Get the rect in which the level is
        for o in self.objects:
            hit_box = o.get_hit_box()
            val_max_x = hit_box.get_max_x()
            val_max_y = hit_box.get_max_y()
            val_min_x = hit_box.get_min_x()
            val_min_y = hit_box.get_min_y()
            if val_max_x > maxi_x:
                maxi_x = val_max_x
            if val_min_x < mini_x:
                mini_x = val_min_x
            if val_max_y > maxi_y:
                maxi_y = val_max_y
            if val_min_y < mini_y:
                mini_y = val_min_y
        self.size_level = (mini_x,maxi_x,mini_y,maxi_y)

    def get_size_level(self):
        return self.size_level
