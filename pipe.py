import pygame
import os
import random

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Birds - Pipes", "pipe_ub2.png")))

class Pipe:
    GAP = 200   # How much space is in between our pipe
    VEL =  5    # How fast our pipes are gonna be moving because since we have the way the flappy
                # bird works essentially is our bird doesn't move but all the objects in the screen
                # move, we need to move the pipes backwards or towards the bird to make it look like it's moving
    def __init__(self, x): # only the x because the height of the pipe will be random.
        self.x = x
        self.height = 0
        # Create variables to keep track of where the top of our pipe is gonna be drawn and where the bottom of our
        # pipe will be drawn.
        self.top = 0
        self.bottom = 0
        # also need a pipe that faces upside down, we've to flip it.
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False # if the bird is already passed by this pipe (for collision proposes and AI)
        self.set_height()

    # This method is gonna define where the top of our pipe is, where the bottom of our pipe is
    # how tall it is
    def set_height(self):
        # Get a random number for where the top of our pipe should be
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    # A method to move our pipes: change the x position based on the velocity that the pipe should move each
    # frame.
    def move(self):
        self.x -= self.VEL # To the left of the screen
    # Draw the top and the bottom of the pipe.
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask() # get bird's mask to compare with pipe mask and see if there's a collision
        # Pipe mask:
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask =pygame.mask.from_surface(self.PIPE_BOTTOM)
        # Compare mask, see if two pixels are overlapping or not:
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # if these two masks collide
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if t_point or b_point: # we're colliding
            return True
        return False
