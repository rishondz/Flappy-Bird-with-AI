import pygame
import os

pygame.font.init() 

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 100)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
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

def end_game(win, score):
    runs = True
    win.blit(bg_img, (0,0))
    text1 = END_FONT.render("GAME OVER", 2, (0, 0, 0))
    win.blit(text1, ((WIN_WIDTH - text1.get_width())//2, (WIN_HEIGHT - text1.get_height())//2 - 100))
    text2 = END_FONT.render(str(score), 2, (0, 0, 0))
    win.blit(text2, ((WIN_WIDTH - text2.get_width())//2, (WIN_HEIGHT - text2.get_height())//2 + text1.get_height() - 50))
    text3 = STAT_FONT.render("Press 'R' to continue", 2, (0, 0, 0))
    win.blit(text3, ((WIN_WIDTH - text3.get_width())//2, WIN_HEIGHT - text3.get_height() - 10))

    pygame.display.update()

    clock = pygame.time.Clock()
    while runs:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runs = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                run()

def run():
    global WIN

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0
    bird = Bird(230,350)
    clock = pygame.time.Clock()
    collided = False
    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if not collided and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
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
    end_game(WIN, score)


if __name__ == "__main__":
    run()