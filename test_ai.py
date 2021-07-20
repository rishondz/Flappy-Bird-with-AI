import pygame
import os
import pickle
import neat

pygame.font.init() 

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 100)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Testing AI")
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

from classes.Bird import Bird
from classes.Pipe import Pipe
from classes.Base import Base

def draw_window(win, bird, pipes, base, score):
    win.blit(bg_img, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    # score
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    pygame.display.update()


def run(net):

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0
    bird = Bird(230,350)
    clock = pygame.time.Clock()
    collided = False
    run = True
    pipe_ind = 0
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            
        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
            pipe_ind = 1
        
        # make bird jump
        action = net.activate((abs(bird.x - pipes[pipe_ind].x), bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
        if action[0] > 0.5:
            bird.jump()
        
        # make bird move
        bird.move()
        base.move()

        # check for collision with floor or top of the screen
        if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
            collided = True
        
        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                collided = True            

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # add pipe at the end of the screen
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)
        if collided:
            run = False
            break
        draw_window(WIN, bird, pipes, base, score)
    


if __name__ == "__main__":
    # load the winner
    with open('winner', 'rb') as f:
        c = pickle.load(f)

    print('Loaded genome:')
    print(c)

    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    net = neat.nn.FeedForwardNetwork.create(c, config)

    run(net)