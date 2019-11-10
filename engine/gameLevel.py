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
        self.physics_resolution = 0.1
        self.collision_objects = []
        self.compute_collision_objects()

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

    def compute_collision_objects(self):
        """ Computes the array to compute collisions in O(1) """
        ref_rect = self.camera.rect #Camera rect
        v = ref_rect.get_dimension()
        offset = self.physics_resolution
        ref_rect.set_dimension( Vector(v.x+2*offset,v.y+2*offset) ) #Add an offset around the camera rect in order to handle physics while the camera is moving
        (min_x,max_x,min_y,max_y) = self.size_level
        size_x = int( (max_x-min_x)/self.physics_resolution ) #Size of the array
        size_y = int( (max_y-min_y)/self.physics_resolution )
        for n in range(size_y):
            self.collision_objects.append([])
            for m in range(size_x):
                self.collision_objects[n].append([])
                #Computes the x and y pos for the camera
                x_pos = m*self.physics_resolution + min_x - offset
                y_pos = n*self.physics_resolution + min_y - offset
                ref_rect.set_position(Vector(x_pos,y_pos))
                for o in self.objects:
                    if o.get_collide() and self.camera.is_in_camera(o.get_hit_box()):
                        self.collision_objects[n][m].append(o) #Store a pointer to objects that are in the camera
