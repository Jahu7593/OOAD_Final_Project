import pygame
import command

class Main():  #acts as INVOKER to command class
    # imports all pygame modules and then initialzes it
    pygame.init()
    
    def launch(self):
        c = command.Command()
        c.start_game()

obj = Main()
obj.launch()
    