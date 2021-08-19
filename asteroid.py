import pygame
import math
from asteroid_classes import *

# Global variables below VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

# Configurable variables:
# Define colors, yay RGB
black	= (0, 0, 0)
white	= (255, 255, 255)
green	= (0, 255, 0)
red		= (255, 0, 0)
blue 	= (0, 0, 255)
gray 	= (200, 200, 200)

# Set width and height of the screen [w,h]
size = [700, 600]

FPS = 60

# Sprite groups:
bullet_group = pygame.sprite.Group()
#fragment_group = pygame.sprite.Group()
#all_sprite = pygame.sprite.LayeredUpdates() # can draw sprites in layers
asteroids = pygame.sprite.Group()
particles = pygame.sprite.Group()
shots = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()

widthheight = [20,20] # of the square around the ship
triangle = [[10,0], [0,20], [20,20]] # x,y coordinates of the corners 

hexwh = [36,36]
hexagon = [[12,0], [24,0], [36,18], [24,36], [12,36], [0,18]]

lives = 3
score = 0

# Global variables above ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Functions below VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

def radians_to_degrees(radians):
	return(radians / math.pi) * 180
def degrees_to_radians(degrees):
	return degrees * (math.pi / 180)

# Functions above ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pygame.init() # Initialize PyGame

screen = pygame.display.set_mode(size) # Setup up the screen
pygame.display.set_caption("asteroid") # Window title

pygame.time.Clock().tick(FPS) # Update screen at (FPS)

# enable key repeat and set to (delay, interval) in milliseconds
pygame.key.set_repeat(50, 50)

# Create the ship:
ship = Ship(green, widthheight, triangle, screen, shots)

all_sprite.add(ship) 

# Create asteroids:
for i in range(7):
	asteroid = Asteroid(gray, hexwh, hexagon, screen)
	
	asteroids.add(asteroid)
	all_sprite.add(asteroid)

done = False # changes to True when we're done..

#  --  Main Program Loop --
while done == False:

	# Event processing below VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
	seconds = pygame.time.Clock().tick(FPS) / 1000
	
	
	
	for event in pygame.event.get():  # The user did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag to end the while loop
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				done = True # Quit the program
		else: 
			break
				
	# Event processing above ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# Game logic below VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
#	milliseconds = clock.tick(
				
	# Game logic above ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# Draw code below VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
	
	# Clear the screen black, don't draw above this:
	screen.fill(black)
	
	ship.update(shots, all_sprite)
	asteroids.update()
	particles.update()
	shots.update()
	
	# Has the player collided with an asteroid?
	asteroid_ship_hit = pygame.sprite.spritecollide(ship, asteroids, False)
	
	for hit in asteroid_ship_hit:
		ship.explode(particles, screen, all_sprite)
		print "We been hit!"
		Ship.remove(ship)
		lives -= 1
		if lives > 0:
			ship = Ship(green, widthheight, triangle, screen, shots)
	
	shots_asteroids_hit = pygame.sprite.groupcollide(asteroids, shots, True, 
		True) # Returns a dict of asteroids to shots values, reference asteroids
	
	for asteroid in shots_asteroids_hit: # The dict is full of asteroid values
		asteroid.explode(particles, screen, all_sprite) #EXPLODE THEM!
		score += 1
		
	# Draw all sprites:
	all_sprite.draw(screen)
		
	# select a font: Default 20 pt.
	font = pygame.font.Font(None, 20)
	
	# Render text.  True = anti aliased
	# only creates an image of the text and assigns it to text
	# text = font.render("My text", True, color) 
	# put the image of the above text somewhere:
	# screen.blit(text, [x, y])
	
	
	score_text = font.render("Score: " + str(score), True, white)
	screen.blit(score_text, [10,10])
	
	# Draw code above ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	
	# Update the screen with the draw code:
	pygame.display.flip()
	
# Close window and quit.  Will hang without this if running from IDLE:
pygame.quit()	