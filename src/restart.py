import pygame
from pygame.locals import *
import random

# imports all pygame modules and then initialzes it
pygame.init()

button_img = pygame.image.load('img/restart.png')
screen = None
screen_width = 864
screen_height = 936


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # need to get the mouse postion
        position = pygame.mouse.get_pos()

        if (self.rect.collidepoint(position)):
            # left most button has been clicked
            if pygame.mouse.get_pressed()[0] == 1:
                # means it has been clicked
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


button = Button(screen_width // 2 - 50, screen_height // 2 - 200,  button_img)
