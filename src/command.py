import pygame
import bird
import pipe
import restart
import scoreObserver
import menu
import game

class Command():
    # imports all pygame modules and then initialzes it
    pygame.init()
    def __init__(self):
        screen_width = 864
        screen_height = 936
        #init screen object
        global screen
        screen = pygame.display.set_mode((screen_width, screen_height))  #this needs to be passed down to "Menu" and "Game"
        restart.screen = screen
        pygame.display.set_caption('Flappy Bird Game')
        
        #init all relevant objects
        global m, g
        m = menu.Menu(screen)
        g = game.Game(screen)

    
    def display_main_menu(self):  #access Menu to display main menu
        m.main_menu()
        return
    
    def update_menu(self):   #access Game to update menu selection (if necessary)
        return
    
    def start_game(self):
        g.start_game()