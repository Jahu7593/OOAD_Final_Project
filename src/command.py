import pygame
# import bird
import pipe
import restart
import scoreObserver
import menu
import game
import screen

class Command():
    # imports all pygame modules and then initialzes it
    
    def __init__(self):
        global restart_condition
        restart_condition = False  

        pygame.display.set_caption('Flappy Bird Game')
        
        #init all relevant objects
        global m, g, scr
        scr = screen.Screen()
        m = menu.Menu(scr)
        g = game.Game(scr)

        self.curr_score = 0
        self.high_score = 0

        global screen_height, screen_width, s
        screen_width = scr.screen_width
        screen_height = scr.screen_height
        s = scr.screen

        global game_stopped
        game_stopped = True
    
    def display_main_menu(self):  #access Menu to display main menu
        m.main_menu(restart_condition, self.curr_score, self.high_score)
        return
    
    def start_game(self):
        global game_stopped
        while game_stopped:   #outer game loop (menu --> game --> menu, handling)
            g.quit_game()
            m.display_images()
            #display main menu
            m.click = False
            self.display_main_menu()
            self.restart_condition = True
            bg_img, bird_img = m.display_images()    #ensures that whatever image selected from menu is displayed to play
            #s.blit(start_image, (screen_width // 2 - start_image.get_width() // 2, screen_height // 2 - start_image.get_height() // 2))
            # User Input
            user_input = pygame.mouse.get_pressed()
            if user_input[0]:
                # bird.clicked = True
                self.curr_score, self.high_score = g.main(bg_img, bird_img)  #get current score\high score from running main (game), pass in selected image
            pygame.display.update()