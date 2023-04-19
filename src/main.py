import pygame
from pygame.locals import *
import random
import bird
import pipe
import restart
# import menu

# imports all pygame modules and then initialzes it
pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
restart.screen = screen
# menu.screen = screen
pygame.display.set_caption('Flappy Bird Game')


# we need a background image for our game:
background_img = pygame.image.load('img/background.png')
ground = pygame.image.load('img/ground.png')

font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)


# This is to write the score to a file/img
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe.pipe_group.empty()
    bird.flappy.rect.x = 100
    bird.flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


def menu():
    print("hello")


def main():
    scroll = 0
    # how many pixels the ground moves
    speed = 4
    # To handle the start of the game
    flying = False
    global start_game
    # this means we'll satrt making pipes right away
    last_pipe = pygame.time.get_ticks() - pipe.pipe_frequency
    run = True
    score = 0
    pass_pipe = False
    high_score = 0
    game_over = False

    # we want to run the game until someone exits out of it
    while run:
        start_game = False
        clock.tick(fps)

        # load the background image into the game
        screen.blit(background_img, (0, 0))

        # add main menu here??

        bird.bird_group.draw(screen)
        bird.bird_group.update()

        pipe.pipe_group.draw(screen)

        # checking the score
        if len(pipe.pipe_group) > 0:
            # checking to see if bird has passed through the left hand side of the pipe
            if bird.bird_group.sprites()[0].rect.left > pipe.pipe_group.sprites()[0].rect.left\
                    and bird.bird_group.sprites()[0].rect.right < pipe.pipe_group.sprites()[0].rect.right\
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                # Has the bird exited the pipe?
                if bird.bird_group.sprites()[0].rect.left > pipe.pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width/2), 20)

        # load the ground image into the game (scrolling background)
        # x coordinate needs to change so that the ground can move
        screen.blit(ground, (scroll, 768))

        # This checks to see if the bird has collided with the pipe
        if pygame.sprite.groupcollide(bird.bird_group, pipe.pipe_group, False, False) or bird.flappy.rect.top < 0:
            game_over = True
            bird.Bird.game_over = game_over

        # checking if the bird has hit the ground:
        if bird.flappy.rect.bottom >= 768:
            game_over = True
            bird.Bird.game_over = game_over
            flying = False
            bird.Bird.flying = flying

        if game_over == False and flying == True:
            # generate new pipes
            last_pipe = pipe.new_pipes(last_pipe)

            scroll -= speed
            # This ensures that the ground looks like it's continuously moving
            if abs(scroll) > 35:
                scroll = 0

            # we only want to update the pipes when the game is running
            pipe.pipe_group.update()

        # checking if the game is over or we need to reset
        if game_over == True:
            if score > high_score:
                high_score = score
                print("high score:", high_score)
            if restart.button.draw() == True:
                # game has been restarted but isn't over
                game_over = False
                bird.Bird.game_over = game_over
                start_game = False
                score = reset_game()

        for event in pygame.event.get():
            # if someone selects the exit out of the game button
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                flying = True
                bird.Bird.flying = flying

        pygame.display.update()

    pygame.quit()


main()
