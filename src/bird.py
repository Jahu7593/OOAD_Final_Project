import pygame
from pygame.locals import *
import random

# imports all pygame modules and then initialzes it
pygame.init()

# https://www.pygame.org/docs/ref/sprite.html

# will we need to change this for the observer patter? (if we're doing it)

class Bird(pygame.sprite.Sprite):

    flying = True
    game_over = False

    def __init__(self, x, y):
        # has update and draw built into it
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        # speed of animation
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        # we use this to set the boundraies of our bird image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # for the physics of the game
        self.velocity = 0
        self.clicked = True

    def game_physics(self):

        if (Bird.flying == True):
            # How we want the bird to "bounce" -> gravity
            self.velocity += 0.5
            if self.velocity > 5:
                self.velocity = 5

            if (self.rect.bottom < 768):
                self.rect.y += int(self.velocity)

        # https://www.pygame.org/docs/ref/mouse.html
        # checking if mouse is clicked
        if (Bird.game_over == False):
            if (pygame.mouse.get_pressed()[0] == 1) and (self.clicked == False):
                self.clicked = True
                self.velocity = -10

            # checking if mouse is released
            if (pygame.mouse.get_pressed()[0] == 0):
                self.clicked = False

    def update(self):

        self.game_physics()

        # handles the animation for the game
        if (Bird.game_over == False):
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # rotating the bird
            self.image = pygame.transform.rotate(
                self.images[self.index], self.velocity * -2)
        else:
            # bird faces the ground
            self.image = pygame.transform.rotate(
                self.images[self.index], -90)


bird_group = pygame.sprite.Group()
flappy = Bird(100, int(936/2))
bird_group.add(flappy)
