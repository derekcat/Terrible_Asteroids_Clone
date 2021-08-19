import pygame
import math
import random

GRAD = math.pi /180 # 1 degree, in Radiants. (not a gradient...)
white	= (255, 255, 255)
red		= (255, 0, 0)
yellow 	= (255, 255, 0)
gray 	= (180, 180, 180)

size = [700, 600]

def loopwindow(self):
	# loop around window
	# if it's off the right, move to left edge
	if self.pos[0] > (size[0] - self.rect[2]): 
		self.pos[0] = 0
	# or if it's off the left, move to the right edge
	elif self.pos[0] < 0:
		self.pos[0] = (size[0] - self.rect[2])
		
	# if it's off the bottom, move to the top edge
	if self.pos[1] > (size[1] - self.rect[3]):
		self.pos[1] = 0
	# if it's off the top, move to the bottom edge
	elif self.pos[1] < 0:
		self.pos[1] = (size[1] - self.rect[3])


class Ship(pygame.sprite.Sprite):
	def __init__(self, color, widthheight, triangle, screen, shots):
		pygame.sprite.Sprite.__init__(self) # obligatory parent class call

		# Dimensions of a rect around the ship
		self.image_master = pygame.Surface(widthheight) #create surface

		self.image_master.fill(white) # fill background of the surface
		self.image_master.set_colorkey(white) # Chroma key background
		# draw the ship's shape ON the surface above
		pygame.draw.polygon(self.image_master, color, triangle, 0)
		
		# Copy the surface? [I think]
		self.image = self.image_master

		# get the rect obj. with dimensions of the image, position via:
		# rect.x or rect.y
		self.rect = self.image.get_rect() # A reference?  Pointer?

		self.pos = [screen.get_width()/2, screen.get_height()/2]
		# sets the surface's center's coordinates	
		self.rect.center = self.pos
		
		self.movementx = 0.0
		self.movementy = 0.0
		self.angle = 0.0
		self.rotatespeed = 5.0

		self.dead = 0 # 0 = alive, !0 = dead
			
	def rotate(self):
		# Rotate:
		if self.pressedkeys[pygame.K_LEFT]:
			self.angle += self.rotatespeed # turn counter clockwise
			if self.angle > 360: # don't let the angle spiral past 360
				self.angle = 0
		if self.pressedkeys[pygame.K_RIGHT]:
			self.angle -= self.rotatespeed
			if self.angle < -360: # don't let the angle spiral below -360
				self.angle = 0
				
	def update(self, shots, all_sprite):
		self.pressedkeys = pygame.key.get_pressed()

		# Acceleration:	
		self.accelx = 0.0
		self.accely = 0.0
		
		if self.pressedkeys[pygame.K_UP]: # Forward, unto the pages of history!
			self.accelx = - math.sin(self.angle * GRAD) # Accel at 1px/sec
			self.accely = - math.cos(self.angle * GRAD)
			self.accelx = self.accelx * 0.5 # Limit to 0.5 px/sec
			self.accely = self.accely * 0.5
			self.movementx += self.accelx
			self.movementy += self.accely
		
		# Speed limit:
		if self.movementx > 10: 
			self.movementx = 10
		elif self.movementx < -10:
			self.movementx = -10
			
		if self.movementy > 10:
			self.movementy = 10
		elif self.movementy < -10:
			self.movementy = -10
		
		# Rotate:
		self.rotate()

		# Turn around:
#		if self.pressedkeys[pygame.K_DOWN]:
#			if - self.movementx != - (math.sin(self.angle * GRAD) + self.movementx) + 1:
#				self.angle += self.rotatespeed # turn counter clockwise
#			if self.angle > 360: # don't let the angle spiral past 360
#				self.angle = 0


		# Shooting:
		if self.pressedkeys[pygame.K_SPACE] and self.dead == 0:
			print("Space has been pressed")
			shell = Shot(self.angle, self.pos)
			shots.add(shell)
			all_sprite.add(shell)

		# save the surface's center coordinates
		old_center = self.rect.center
	
		# Transform the copy of the surface
		self.image = pygame.transform.rotate(self.image_master, self.angle)
		
		# Re-get the surface's dimensions
		self.rect = self.image.get_rect()
		# Re-center using the saved coordinates
		self.rect.center = old_center
		
		self.pos[0] += self.movementx
		self.pos[1] += self.movementy
		
		self.rect.center = self.pos
		loopwindow(self)
		
	
#		print "math.sin(self.angle * GRAD): ", math.sin(self.angle * GRAD) + self.movementx
		print("-math.sin(self.angle * GRAD): ", - (math.sin(self.angle * GRAD) + self.movementx) + 1)
		print("angle: ", self.angle) #test code
		print("accelx: ", self.accelx)
		print("accely: ", self.accely)
		print("movementx: ", self.movementx)
		print("movementy: ", self.movementy)
#		print "rect.x: ", self.rect.x
#		print "rect.y: ", self.rect.y
	
	def explode(self, particles, screen, all_sprite):
		if self.dead == 0: # If not dead
			for i in range(50):
				particle = Particle(red, [2,2], [[0,0], [0,2], [2,2], [2,0]],
				 screen, self.pos)
				particles.add(particle)
				all_sprite.add(particle)
			pygame.sprite.Sprite.kill(self)
			self.dead = 1
				
	
class Asteroid(pygame.sprite.Sprite):
	def __init__(self, color, widthheight, shape, screen):
		pygame.sprite.Sprite.__init__(self) # obligatory parent class call

		# Dimensions of a rect around the ship
		self.image_master = pygame.Surface(widthheight) #create surface

		self.image_master.fill(white) # fill background of the surface
		self.image_master.set_colorkey(white) # Chroma key background
		# draw the ship's shape ON the surface above
		pygame.draw.polygon(self.image_master, color, shape, 0)
		
		# Copy the surface? [I think]
		self.image = self.image_master

		# get the rect obj. with dimensions of the image, position via:
		# rect.x or rect.y
		self.rect = self.image.get_rect() # A reference?  Pointer?

		self.pos = [random.randrange(0, screen.get_width()), \
				random.randrange(0, screen.get_height()/2)]
		# sets the surface's center's coordinates	
		self.rect.center = self.pos
		
		self.movementx = random.randrange(-2,3)
		if self.movementx == 0: # Stopped asteroids would we weird..
			self.movementx = random.randrange(-2,3)

		self.movementy = random.randrange(-2,3)
		if self.movementy == 0:
			self.movementy = random.randrange(-2,3)

		# Spin
		self.angle = 0.0
		self.rotatespeed = random.random() * random.randrange(1,3)
		if self.rotatespeed >= 0.1:
			self.rotatespeed = random.random() * random.randrange(1,3)
	
	
	def update(self):
		# save the surface's center coordinates
		old_center = self.rect.center
	
		# Transform the copy of the surface
		self.image = pygame.transform.rotate(self.image_master, self.angle)
		
		# Re-get the surface's dimensions
		self.rect = self.image.get_rect()
		# Re-center using the saved coordinates
		self.rect.center = old_center
		
		self.pos[0] += self.movementx
		self.pos[1] += self.movementy
		
		self.rect.center = self.pos
		loopwindow(self)
		
		# Spinning
		self.angle += self.rotatespeed
		if self.angle > 360:
			self.angle = 0
			
	def explode(self, particles, screen, all_sprite):
		for i in range(50):
			particle = Particle(gray, [2,2], [[0,0], [0,2], [2,2], [2,0]],
			 screen, self.pos)
			particles.add(particle)
			all_sprite.add(particle)
		pygame.sprite.Sprite.kill(self)
		
		
class Particle(pygame.sprite.Sprite):
	def __init__(self, color, widthheight, shape, screen, start_pos):
		pygame.sprite.Sprite.__init__(self) # obligatory parent class call

		# life kill death counter
		self.lifetimer = 0

		# random colors:
#		color = (random.randrange(100,256), random.randrange(100,256), random.randrange(100,256))

		# Dimensions of a rect around the particle
		self.image_master = pygame.Surface(widthheight) #create surface

		self.image_master.fill(white) # fill background of the surface
		self.image_master.set_colorkey(white) # Chroma key background
		# draw the particle's shape ON the surface above
		pygame.draw.polygon(self.image_master, color, shape, 0)
	
		# Copy the surface? [I think]
		self.image = self.image_master

		# get the rect obj. with dimensions of the image, position via:
		# rect.x or rect.y
		self.rect = self.image.get_rect() # A reference?  Pointer?

		# sets the surface's center's coordinates	
		self.rect.center = start_pos
	
		# Set the speed
		self.angle = random.randrange(0,361)
		self.movementx = - math.sin(self.angle * GRAD) * random.randrange(1,10)

		self.angle = random.randrange(0,361)
		self.movementy = - math.cos(self.angle * GRAD) * random.randrange(1,10)
		

	def update(self):
		self.rect.x += self.movementx
		self.rect.y += self.movementy

		# increment life time, delete after 200 updates
		self.lifetimer += 1
		if self.lifetimer == 200:
			pygame.sprite.Sprite.kill(self)
		
class Shot(pygame.sprite.Sprite):
	def __init__(self, angle, start_pos):
		pygame.sprite.Sprite.__init__(self) # obligatory parent class call

		#life of the shot
		self.lifetimer = 0
				
		# Dimensions of a rect around the shot
		self.image_master = pygame.Surface([5,5]) #create surface

		self.image_master.fill(white) # fill background of the surface
		self.image_master.set_colorkey(white) # Chroma key background
		# draw the particle's shape ON the surface above
		pygame.draw.polygon(self.image_master, yellow, 
				[[0,0], [0,5], [5,5], [5,0]], 0) # 5x5 square shots
	
		# Copy the surface? [I think]
		self.image = self.image_master

		# get the rect obj. with dimensions of the image, position via:
		# rect.x or rect.y
		self.rect = self.image.get_rect() # A reference?  Pointer?

		# sets the surface's center's coordinates	
		self.rect.center = start_pos
	
		# Set the speed
		self.movementx = - math.sin(angle * GRAD) * 7
		self.movementy = - math.cos(angle * GRAD) * 7
		
		
		
	def update(self):
		self.rect.x += self.movementx
		self.rect.y += self.movementy

		# increment life time, delete after some number of updates
		self.lifetimer += 1
		if self.lifetimer == 75:
			pygame.sprite.Sprite.kill(self)
			
		# loop around window
		# if it's off the right, move to left edge
		if self.rect.x > (size[0] - self.rect[2]): 
			self.rect.x = 0
		# or if it's off the left, move to the right edge
		elif self.rect.x < 0:
			self.rect.x = (size[0] - self.rect[2])
		
		# if it's off the bottom, move to the top edge
		if self.rect.y > (size[1] - self.rect[3]):
			self.rect.y = 0
		# if it's off the top, move to the bottom edge
		elif self.rect.y < 0:
			self.rect.y = (size[1] - self.rect[3])