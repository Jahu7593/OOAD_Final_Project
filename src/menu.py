import pygame
from pygame.locals import *
import random
import main

# imports all pygame modules and then initialzes it
pygame.init()


button_img = pygame.image.load('img/start.png')
skyline_image = pygame.image.load('img/background.png')
ground_image = pygame.image.load('img/ground.png')
# top_pipe_image = pygame.image.load('img/pipe.png')
# bottom_pipe_image = pygame.image.load('img/pipe_bottom.png')
# game_over_image = pygame.image.load('img/game_over.png')
start_image = pygame.image.load('img/start.png')
screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))


class Menu(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # need to get the mouse postion
        position = pygame.mouse.get_pos()

        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.fill((0, 0, 0))
        screen.blit(skyline_image, (0, 0))
        screen.blit(ground_image, (0, 520))
        # screen.blit(bird_images[0], (100, 250))
        screen.blit(start_image, (screen_width // 2 - start_image.get_width() // 2,
                                  screen_height // 2 - start_image.get_height() // 2))

        if (self.rect.collidepoint(position)):
            # left most button has been clicked
            if pygame.mouse.get_pressed()[0] == 1:
                # means it has been clicked
                main.main()
                action = True

        return action

    def update(self):
        self.image = None


menu = Menu(screen_width // 2 - 50, screen_height // 2 - 100,  button_img)
menu.draw()
