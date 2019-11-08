import Camera

class GameLevel:
    def __init__(self,objects):
        self.camera = Camera()
        self.objects = objects
        self.physics_resolution = 0.1

    def optimize_objects(self):
        ref_rect = Camera.rect
        for o in objects:
            objects.polygon.point_in(
