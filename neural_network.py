import pygame
import neat
import os
import random
from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init() # initialize font for the score


GEN = 0

# set the size of the screen:
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Now we're going to load all the images:
# pygame.image.load -> loads the image
# pygame.transform.scale2x -> makes the image bigger

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png"))) # Background image

STAT_FONT = pygame.font.SysFont("Arial", 20) # to the score
'''
A function to deleate the bird, the genome and the neural network of
index ind.
'''
def delete_genome(ind, birds, nets, gen):
    birds.pop(ind) # and remove this bird
    nets.pop(ind)
    gen.pop(ind)


def draw_window(win, birds, pipes, base, score, gen, population_size, n_alive): # draw our game screen
    win.blit(BG_IMG, (0,0))# blit means draw; 0,0 is the top left position
    for pipe in pipes: # draw each pipe
        pipe.draw(win)
    # Show population value
    text = STAT_FONT.render("Population Size: " + str(population_size), 1, (255,255,255))
    win.blit(text, (10, 10))
    # Show generation value
    text = STAT_FONT.render("Generation: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 40))
    # Show score value
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (10, 70))
    # Show the number of current birds alive
    text = STAT_FONT.render("Alive: " + str(n_alive), 1, (255,255,255))
    win.blit(text, (10, 100))

    base.draw(win) # draw the floor
    for bird in birds:
        bird.draw(win) # draw the bird

    pygame.display.update()


def new_generation(genomes, config):
    global GEN
    GEN += 1
    nets = []
    gen = []
    birds = []
    # set the birds' generation color
    random_color = random.randint(0,2) # 3 colors to choose
    # set up our neural network
    for _, genome in genomes: # genomes is a tuple that have the genome ID and the genome object
        net = neat.nn.FeedForwardNetwork.create(genome, config) # Give to neural network the genome and the config file
        nets.append(net) # append it in list
        birds.append(Bird(230, 350, random_color)) # append the bird
        genome.fitness = 0 # function value initial in zero
        gen.append(genome) # append the genome in the same positions as the bird and the neat
    # Save the population size to display it later
    population_size = len(birds)
    # bird = Bird(230,350) # create a bird
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) # Create the window
    clock = pygame.time.Clock() # we need a clock for framerate
    run = True # game is running
    score = 0 # Points. It will be increase when a bird pass a pipe.
    goal = 100 # Set 100 as goal. When the score arrives to this value, the game finishes.
    # Game/main loop
    while run:
        clock.tick(30) # 30 ticks every second
        for event in pygame.event.get(): # when users press a key or click a mouse
            if event.type == pygame.QUIT: # quit the game when X red in the window is pressed
                run = False
                pygame.quit()
                quit()
        # bird.move()

        # we need to check what pipe (of the two pipes at maximum that can be in the screen)
        # is going to pass the bird, if is the first pipe in the list or the second, to
        # calculate the distance in axis y
        pipe_ind = 0 # we looking at the first pipe as the input in neural network
        if len(birds) > 0: # there're birds
            # if there is more than 1 pipe (2 pipes) and the position of the bird in axis x is
            # greater than the first pipe's position (plus his width), means that the bird
            # has passed the first pipe and we've to consider the second pipe for the fitness function
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1 # we looking at the second pipe as the input in neural network
        else: # if there aren't bird we want to finish this generation
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            # We sum 0.1 at fitness function of the bird's genome for survive. Rememeber that
            # these game have 30 frames at second and these value is going to sum 30 times every loop
            gen[x].fitness += 0.1
            # calculate the output, if the bird jump or not, passing as input the position's bird, the distance between the bird and the top of
            # the pipe and the distance between the bird and the bottom of the pipe.
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            # see if the output is greater than 0.5
            if output[0] > 0.5: # output is a list of output neurons, but in our case we've only one neuron
                bird.jump() # bird have to jump


        add_pipe = False
        rem = [] # list of objects to remove
        for pipe in pipes: # move the pipes
            # Check the following conditions for each bird (x: bird position, bird: object)
            for ind, bird in enumerate(birds):
                if pipe.collide(bird): # check if the bird collides the current pipe
                    # every time a bird collides with a pipe, the genome of this bird is gonna remove
                    # one point of his fitness score
                    gen[ind].fitness -= 1
                    delete_genome(ind, birds, nets, gen)

                if not pipe.passed and pipe.x < bird.x: # Check if the bird passed the pipe
                    pipe.passed = True
                    add_pipe = True # we have to generate another pipe
            if pipe.x + pipe.PIPE_TOP.get_width() < 0: # Check if our pipe is completely out the screen
                rem.append(pipe)

            pipe.move()
        if add_pipe: # update the score and generate another pipe
            score += 1
            for g in gen: # See each genome
                # If the genome is currently in the list of genomes, it means that the bird survive
                # (doesn't collide with a pipe) and we add 5 points to his fitness function score.
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem: # remove the pipes that completly go out of the screen
            pipes.remove(r)
        for ind, bird in enumerate(birds):
            # check if the bird hit to the floor or is upward the pipes and the screen
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0: # 730 = height of the floor
                delete_genome(ind, birds, nets, gen)
        # Check if the bird arrives to the goal.
        if score >= goal: # 100
            print(f"The generation {GEN-1} arrives to the goal!!!")
            break # finish this generation

        base.move() # move the floor
        draw_window(win, birds, pipes, base, score, GEN, population_size, len(birds))
        # Pass as alive the current size of birds that is equal to the birds alive (we remove the collisioned birds).


# main()

# Run NEAT
def run_NEAT(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config) # Population
    # See in console some stadistics about each generation
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(new_generation,40) # 40 generations we are going to run the fitness function, that
    # means it is gonna call the main function 40 times.

# Set configuration NEAT document
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run_NEAT(config_path)
