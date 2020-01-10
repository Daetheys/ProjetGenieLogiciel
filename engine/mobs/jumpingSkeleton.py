from engine.mobs.zombie import *

class JumpingSkeleton(Zombie):
	def __init__(self):
		super().__init__()
		self.controller = JumpingSkeletonController(self)

class JumpingSkeletonController(MobController):
	def __init__(self,target=None):
		super().__init__()
		self.target = target
		self.period = 2

	def execute(self,event,pressed,dt):
		super().execute(event,pressed,dt)
		self.target.set_speedx(10)
		if self.target.alive:
			self.target.move(dt)
		if (self.target.world.time%self.period) < dt:
			self.timer = self.target.world.time
			self.jump(0.06)
