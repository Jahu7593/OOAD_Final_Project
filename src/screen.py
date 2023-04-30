import pygame
import restart

class Screen(object):   #may want to destroy & reinstantiate this object every run.
    def __init__(self):
        self.screen_width = 864
        self.screen_height = 936
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))  #this needs to be passed down to "Menu" and "Game"
        restart.screen = screen
        self.screen = screen
        print("Screen object initialized")

