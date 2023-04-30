import pygame
import bird
import pipe
import restart
import scoreObserver
import command
import screen

class Menu(screen.Screen):  #Concrete menu implementation, controlled by Command
    # imports all pygame modules and then initialzes it
    pygame.init()
    #Restart condition - False only for first menu display
    def __init__(self, x):
        self.screen_height = x.screen_height
        self.screen_width = x.screen_width
        self.screen = x.screen
        print(self.screen_height)
        #init fonts/colors
        global font, small_font, white, orange
        font = pygame.font.SysFont('Bauhaus 93', 60)
        small_font = pygame.font.SysFont('Bauhaus 93', 35)
        white = (255, 255, 255)
        orange = (255, 124, 31)
        global location_selected, bird_selected
        location_selected = 0
        bird_selected = 0   #start w/ standard "Flappy" in standard "City"
        #for now storing locations/birds list here, may want to pass in from elsewhere later
        global locations_list, birds_list
        locations_list = ["City"]
        birds_list = ["Flappy"], ["Cessna"]
        
        print("Menu Object Initialized")

    @staticmethod
    def draw_text(text, font, text_col, x, y, self):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
    
    def main_menu(self, restart_condition):
        if restart_condition == True:
            btn1_string = "Restart"
        else:
            btn1_string = "Start"
            restart_condition = True

        while True: # Draw Main Menu
            #get mouse pointer position
            mx, my = pygame.mouse.get_pos()
            #get width/length of text for centering
            fb_width, fb_height = font.size("FLAPPY BIRD")    
            start_width, start_height = small_font.size(btn1_string)
            options_width, options_height = small_font.size("Options")
            exit_width, exit_height = small_font.size("Exit")
            #Set positions
            button_width = 200
            button_height = 50
            title_y = int(self.screen_height/2 - fb_height/2 - 300)
            b1x = int(self.screen_width/2 - button_width/2)   #center x
            b1y = title_y + 100    #y below title
            b2y = b1y + button_height + 30
            b3y = b1y + 2*button_height + 60
            #initialize buttons
            button1 = pygame.Rect(b1x, b1y, button_width, button_height)   #(x, y, width, height)
            button2 = pygame.Rect(b1x, b2y, button_width, button_height)
            button3 = pygame.Rect(b1x, b3y, button_width, button_height)
            #draw buttons
            pygame.draw.rect(self.screen, orange, button1, 0, 15)
            pygame.draw.rect(self.screen, orange, button2, 0, 15)
            pygame.draw.rect(self.screen, orange, button3, 0, 15)
            #draw white borders around buttons
            pygame.draw.rect(self.screen, white, pygame.Rect(b1x, b1y, button_width, button_height), 5, 15)
            pygame.draw.rect(self.screen, white, pygame.Rect(b1x, b1y + button_height + 30, button_width, button_height), 5, 15)
            pygame.draw.rect(self.screen, white, pygame.Rect(b1x, b1y + 2*button_height + 60, button_width, button_height), 5, 15)
            #draw text
            self.draw_text("FLAPPY BIRD", font, white, int(self.screen_width/2 - fb_width/2), title_y, self)  #draw "Flappy Bird" title
            self.draw_text(btn1_string, small_font, white, int(self.screen_width/2 - start_width/2), b1y + 5, self)  
            self.draw_text("Options", small_font, white, int(self.screen_width/2 - options_width/2), b2y + 5, self)  
            self.draw_text("Exit", small_font, white, int(self.screen_width/2 - exit_width/2), b3y + 5, self)  
            #check for clicks on buttons
            if button1.collidepoint((mx, my)):   #Start button returns to game loop
                if click:
                    return
            if button2.collidepoint((mx, my)):   #Options button opens options menu
                if click:
                    self.options_menu()
            if button3.collidepoint((mx, my)):   #Exit button quits the program (or escape)
                if click:
                    event.type = pygame.QUIT
            
            #event listner
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        event.type = pygame.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
        
    def options_menu(self):
        while True: # Draw Options Menu
            global location_selected, bird_selected   #need global keywork (again) when assigning to global variable in a local scope
            location_str = locations_list[location_selected]
            bird_str = birds_list[bird_selected]
            #get mouse pointer position
            mx, my = pygame.mouse.get_pos()
            #get width/length of text for centering
            fb_width, fb_height = font.size("FLAPPY BIRD")    
            location_width, location_height = small_font.size(location_str)
            birdname_width, birdname_height = small_font.size(bird_str)
            back_width, back_height = small_font.size("Back")
            #Set positions
            button_width = 200
            button_height = 50
            title_y = int(self.screen_height/2 - fb_height/2 - 300)
            b1x = int(self.screen_width/2 - button_width/2)   #center x
            b1y = title_y + 100    #y below title
            b2y = b1y + button_height + 30
            b3y = b1y + 2*button_height + 60
            #initialize buttons
            left_button1 = pygame.draw.polygon(self.screen, orange, [[b1x-50, b1y+(button_height/2)], [b1x, b1y+button_height], [b1x, b1y]], 0)
            right_button1 = pygame.draw.polygon(self.screen, orange, [[b1x+button_width+50, b1y+(button_height/2)], [b1x+button_width, b1y+button_height], [b1x+button_width, b1y]], 0)
            left_button2 = pygame.draw.polygon(self.screen, orange, [[b1x-50, b2y+(button_height/2)], [b1x, b2y+button_height], [b1x, b2y]], 0)
            right_button2 = pygame.draw.polygon(self.screen, orange, [[b1x+button_width+50, b2y+(button_height/2)], [b1x+button_width, b2y+button_height], [b1x+button_width, b2y]], 0)
            button5 = pygame.Rect(b1x, b3y, button_width, button_height)
            #draw 2 orange backgrounds (for birdname and location)
            pygame.draw.rect(self.screen, orange, pygame.Rect(b1x, b1y, button_width, button_height), 0, 15)
            pygame.draw.rect(self.screen, orange, pygame.Rect(b1x, b1y + button_height + 30, button_width, button_height), 0, 15)
            #draw button 5 (back)
            pygame.draw.rect(self.screen, orange, button5, 0, 15)
            #draw white borders around buttons
            pygame.draw.rect(self.screen, white, pygame.Rect(b1x, b1y, button_width, button_height), 5, 15)
            pygame.draw.rect(self.screen, white, pygame.Rect(b1x, b1y + button_height + 30, button_width, button_height), 5, 15)
            pygame.draw.rect(self.screen, white, pygame.Rect(b1x, b1y + 2*button_height + 60, button_width, button_height), 5, 15)
            #draw text
            self.draw_text("FLAPPY BIRD", font, white, int(self.screen_width/2 - fb_width/2), title_y, self)  #draw "Flappy Bird" title
            self.draw_text(location_str, small_font, white, int(self.screen_width/2 - location_width/2), b1y + 5, self)  
            self.draw_text(bird_str, small_font, white, int(self.screen_width/2 - birdname_width/2), b2y + 5, self)  
            self.draw_text("Back", small_font, white, int(self.screen_width/2 - back_width/2), b3y + 5, self)  
            #check for clicks on buttons
            if left_button1.collidepoint((mx, my)):   #Left through MAPS list
                if click:
                    if(location_selected == 0):
                        location_selected = len(locations_list) - 1
                    else:
                        location_selected -= 1
            if right_button1.collidepoint((mx, my)):   #Right through MAPS list
                if click:
                    if(location_selected == len(locations_list)-1):
                        location_selected = 0
                    else:
                        location_selected += 1
            if left_button2.collidepoint((mx, my)):   #Left through BIRDS list
                if click:
                    if(bird_selected == 0):
                        bird_selected = len(birds_list) - 1
                    else:
                        bird_selected -= 1
            if right_button2.collidepoint((mx, my)):   #Right through BIRDS list
                if click:
                    if(bird_selected == len(birds_list)-1):
                        bird_selected = 0
                    else:
                        bird_selected += 1
            if button5.collidepoint((mx, my)):   #Back button returns to main_menu
                if click:
                    #load the same images as selected previously
                    img = pygame.image.load("img/background.png")  #destroy triangles by drawing over w/ location and bird
                    self.screen.blit(img, (0, 0))
                    bird = pygame.image.load("img/Flappy1.png")
                    self.screen.blit(bird, (100, int(self.screen_height/2)))
                    return
            
            #event listner
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        event.type = pygame.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()

