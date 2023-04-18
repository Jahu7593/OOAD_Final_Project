import pygame
from pygame.locals import *
import random

# imports all pygame modules and then initialzes it
pygame.init()

# gap between the two pipes
pipe_gap = 150
scroll_speed = 4
# one and half seconds (milliseconds)
pipe_frequency = 1500
# Measure of time since game has started


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()

        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


def new_pipes(last_pipe):
    time_now = pygame.time.get_ticks()
    if (time_now - last_pipe > pipe_frequency):
        # need to make pipes show up at different heights/places
        pipe_height = random.randint(-100, 100)
        btm_pipe = Pipe(864, int(936 / 2) + pipe_height, -1)
        top_pipe = Pipe(864, int(936 / 2) + pipe_height, 1)
        pipe_group.add(btm_pipe)
        pipe_group.add(top_pipe)
        last_pipe = time_now
    return last_pipe


pipe_group = pygame.sprite.Group()
