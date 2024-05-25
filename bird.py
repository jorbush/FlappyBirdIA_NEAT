import pygame
import os

# Now we're going to load all the images:
BIRD_WHITE_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("Birds - Pipes", "bird1_white.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join("Birds - Pipes", "bird2_white.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join("Birds - Pipes", "bird3_white.png")))]
# pygame.image.load -> loads the image
# pygame.transform.scale2x -> makes the image bigger
BIRD_YELLOW_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
BIRD_PINK_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("Birds - Pipes", "bird1_pink.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join("Birds - Pipes", "bird2_pink.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join("Birds - Pipes", "bird3_pink.png")))]

# Let's go to pragramming our first class which is the bird class.
# It would represents the bird's movements.
# We need a class because later we're going to create a buch differents birds for AI.
class Bird:
    IMGS = [BIRD_YELLOW_IMGS, BIRD_PINK_IMGS, BIRD_WHITE_IMGS] # random.choice([BIRD_YELLOW_IMGS, BIRD_PINK_IMGS, BIRD_WHITE_IMGS])
    # How much the bird is going to rotate when the bird go up or down
    MAX_ROTATION = 25 # in degrees
    # How much we're going to rotate for each frame or every time we move the bird.
    ROT_VEL = 20
    # How long we're going to show each animation, changing this we change how faster or slower
    # the bird flaps his wings.
    ANIMATION_TIME = 5

    def __init__(self, x, y, r):
        # x and y starting position of the bird
        self.x = x
        self.y = y
        # How much the images actually tilted. Inicialize it to zero because we start with the bird flat and
        # we started to moving it.
        self.tilt = 0
        self.tick_count = 0 # count the physics when we jump or fall down
        self.vel = 0 # velocity starts at 0 because is no moving
        self.height = self.y
        self.img_count = 0 # for indexing the bird's images (the list), the bird that we're currently showing
        self.images = self.IMGS[r]
        self.img = self.images[0]
    # We call this method when we need the bird to flap/jump up.
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0 # this keep track when we do the last jump.
        # Is setted to zero because we need to known how change the directions and velocities
        # for the physic formulas in the next method.
        self.height = self.y # where the bird start to jump.
    # We call "move" every single frame for move our bird.
    def move(self):
        # A tick happened a frame went by and now we've moved so we'll keep track of X. How many times
        # we move since the last jump.
        self.tick_count += 1
        # Calculate desplacement (how many pixels were moving up or down this frame and this will be what
        # we end up actually moving when we change the Y position of the bird):
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 # physic equation
        # self.vel*self.tick_count -> We use "tick_count" to represent how many seconds we've been moving for
        # (multiplies velocity and seconds and you obtain distance).
        # 1.5*self.tick_count**2 -> We use this to calculate the arc of the bird (at first it goes up and
        # then it goes down, completing the arc)

        if d >= 16: # if we're moving down more  or equal than 16 pixels
            d = 16 # just move down 16 pixels (set a limit)

        if d < 0: # if we're moving upwards:
            d -= 2 # let's just move up a little bit more

        self.y = self.y + d # updates bird position adding this desplacement (can be upwards or downwards)

        if d < 0 or self.y < self.height + 50:
            # d < 0 => is moving upwards;
            # or self.y < self.height + 50 => if we're on a downward curve
            # so don't start falling yet
            if self.tilt < self.MAX_ROTATION: # if tilt the bird is completely backwards or crazy directions
                self.tilt = self.MAX_ROTATION # Correct the rotation
        else: # if we're not moving upwards and we don't want to tilt the bird upwards
            # let's tilt the bird downwards
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL # this allows us to do is rotate the flappy bird completely 90 degrees

    def draw(self, win): # win is the window where we draw the bird
        # We keep track of how many ticks we've shown a current image, how many times have we already shown one image
        # in the main/game loop.
        self.img_count += 1
        # Check what image we should show based on the current image count. To have the bird flapping.
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.images[0]
        elif self.img_count < self.ANIMATION_TIME*2: # *1
            self.img = self.images[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.images[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.images[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1: # reset image count
            self.img = self.images[0]
            self.img_count = 0
        # if we're falling in 90 degrees, we don't want to shown the bird flapping his wings
        if self.tilt <= -80:
            self.img = self.images[1]
            self.img_count = self.ANIMATION_TIME*2 # To show the same picture the next draw *1
        # rotate the image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # this looks a little weird, we've to correct teh rotation:
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self): # when we get a collision
        return pygame.mask.from_surface(self.img)
