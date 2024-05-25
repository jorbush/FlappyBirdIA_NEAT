import pygame
import os

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png"))) # ground

class Base: # ground
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # the two bases go to the left
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # if one of them disappear out the screen, put it following the base that didn't disappeared.
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win): # draw the two bases
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
