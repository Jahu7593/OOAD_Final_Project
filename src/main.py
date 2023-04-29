import pygame
import command

class Main():  #acts as INVOKER to command class
    # imports all pygame modules and then initialzes it
    pygame.init()
    
    def __init__(self):
        global c
        c = command.Command()
    def startGame(self):
        c.display_main_menu()
        c.start_game()

obj = Main()
obj.startGame()
    