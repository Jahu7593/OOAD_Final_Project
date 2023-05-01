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
        #init fonts/colors
        global font, small_font, white, orange
        font = pygame.font.SysFont('Bauhaus 93', 60)
        small_font = pygame.font.SysFont('Bauhaus 93', 35)
        white = (255, 255, 255)
        orange = (255, 124, 31)
        self.location_selected = 0
        self.bird_selected = 0   #start w/ standard "Flappy" in standard "City"
        #for now storing locations/birds list here, may want to pass in from elsewhere later
        self.locations_list = ["City", "Desert", "Jungle", "Beach"]
        self.birds_list = ["Flappy", "Cessna", "Eagle"]
        global click
        self.click = False
        
        print("Menu Object Initialized")

    @staticmethod
    def draw_text(text, font, text_col, x, y, self):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
    
    def display_images(self):   #function for each initial menu loading
        bg_str = "img/" + self.locations_list[self.location_selected].lower() + ".png"   #selects current background image
        bg_img = pygame.image.load(bg_str)
        bg_img = pygame.transform.scale(bg_img, (864, 768))

        ground_img = pygame.image.load("img/ground.png")
        flappy1_img = pygame.image.load("img/flappy1.png")

        self.screen.fill((0, 0, 0))  #s is screen    #city is 864 x 768
        self.screen.blit(bg_img, (0, 0))
        self.screen.blit(ground_img, (0, 768))
        self.screen.blit(flappy1_img, (100, int(self.screen_height/2)))
        return bg_img
    
    def main_menu(self, restart_condition, curr_score, high_score):
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
            currentscore_width, currentscore_height = small_font.size("Recent Score")
            highscore_width, highscore_height = small_font.size("High Score")
            cs_width, cs_height = font.size(str(curr_score))
            hs_width, hs_height = font.size(str(high_score))
            start_width, start_height = small_font.size(btn1_string)
            options_width, options_height = small_font.size("Options")
            exit_width, exit_height = small_font.size("Exit")
            #Set positions
            button_width = 200
            button_height = 50
            title_y = int(self.screen_height/2 - fb_height/2 - 400)
            b1x = int(self.screen_width/2 - button_width/2)   #center x
            score_y = title_y + 100
            b1y = score_y + 100    #y below title
            b2y = b1y + button_height + 30
            b3y = b1y + 2*button_height + 60
            #Display High Scores
            self.draw_text("Recent Score", small_font, white, int(self.screen_width/2 - currentscore_width/2)-150, score_y-15, self)  
            self.draw_text("High Score", small_font, white, int(self.screen_width/2 - highscore_width/2)+150, score_y-15, self)  
            self.draw_text(str(curr_score), font, white, int(self.screen_width/2 - cs_width/2)-150, score_y+15, self)  
            self.draw_text(str(high_score), font, white, int(self.screen_width/2 - hs_width/2)+150, score_y+15, self)  
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
                if self.click:
                    return
            if button2.collidepoint((mx, my)):   #Options button opens options menu
                if self.click:
                    self.options_menu()
            if button3.collidepoint((mx, my)):   #Exit button quits the program (or escape)
                if self.click:
                    print("Quitting via Exit")
                    pygame.quit()
                    exit()
            
            #event listner
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting via event type QUIT")
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Quitting via Escape")
                        pygame.quit()
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
            pygame.display.update()
        
    def options_menu(self):
        self.click = False
        while True: # Draw Options Menu
            location_str = self.locations_list[self.location_selected]
            bird_str = self.birds_list[self.bird_selected]
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
            title_y = int(self.screen_height/2 - fb_height/2 - 400)
            b1x = int(self.screen_width/2 - button_width/2)   #center x
            b1y = title_y + 200    #y below title
            b2y = b1y + button_height + 30
            b3y = b1y + 2*button_height + 60
            #initialize buttons
            left_button1 = pygame.draw.polygon(self.screen, orange, [[b1x-50, b1y+(button_height/2)], [b1x-10, b1y+button_height-10], [b1x-10, b1y+10]], 0)
            right_button1 = pygame.draw.polygon(self.screen, orange, [[b1x+button_width+50, b1y+(button_height/2)], [b1x+button_width+10, b1y+button_height-10], [b1x+button_width+10, b1y+10]], 0)
            left_button2 = pygame.draw.polygon(self.screen, orange, [[b1x-50, b2y+(button_height/2)], [b1x-10, b2y+button_height-10], [b1x-10, b2y+10]], 0)
            right_button2 = pygame.draw.polygon(self.screen, orange, [[b1x+button_width+50, b2y+(button_height/2)], [b1x+button_width+10, b2y+button_height-10], [b1x+button_width+10, b2y+10]], 0)
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
            #draw white borders around arrows
            pygame.draw.polygon(self.screen, white, [[b1x-50, b1y+(button_height/2)], [b1x-10, b1y+button_height-10], [b1x-10, b1y+10]], 5)
            pygame.draw.polygon(self.screen, white, [[b1x+button_width+50, b1y+(button_height/2)], [b1x+button_width+10, b1y+button_height-10], [b1x+button_width+10, b1y+10]], 5)
            pygame.draw.polygon(self.screen, white, [[b1x-50, b2y+(button_height/2)], [b1x-10, b2y+button_height-10], [b1x-10, b2y+10]], 5)
            pygame.draw.polygon(self.screen, white, [[b1x+button_width+50, b2y+(button_height/2)], [b1x+button_width+10, b2y+button_height-10], [b1x+button_width+10, b2y+10]], 5)
            #draw text
            self.draw_text("FLAPPY BIRD", font, white, int(self.screen_width/2 - fb_width/2), title_y, self)  #draw "Flappy Bird" title
            self.draw_text(location_str, small_font, white, int(self.screen_width/2 - location_width/2), b1y + 5, self)  
            self.draw_text(bird_str, small_font, white, int(self.screen_width/2 - birdname_width/2), b2y + 5, self)  
            self.draw_text("Back", small_font, white, int(self.screen_width/2 - back_width/2), b3y + 5, self)  
            #check for clicks on buttons
            if left_button1.collidepoint((mx, my)):   #Left through MAPS list
                if self.click:
                    if(self.location_selected == 0):
                        self.location_selected = len(self.locations_list) - 1
                    else:
                        self.location_selected -= 1
                    self.display_images()
                    self.options_menu()
            if right_button1.collidepoint((mx, my)):   #Right through MAPS list
                if self.click:
                    if(self.location_selected == len(self.locations_list)-1):
                        self.location_selected = 0
                    else:
                        self.location_selected += 1
                    self.display_images()
                    self.options_menu()
            if left_button2.collidepoint((mx, my)):   #Left through BIRDS list
                if self.click:
                    if(self.bird_selected == 0):
                        self.bird_selected = len(self.birds_list) - 1
                    else:
                        self.bird_selected -= 1
            if right_button2.collidepoint((mx, my)):   #Right through BIRDS list
                if self.click:
                    if(self.bird_selected == len(self.birds_list)-1):
                        self.bird_selected = 0
                    else:
                        self.bird_selected += 1
            if button5.collidepoint((mx, my)):   #Back button returns to main_menu
                if self.click:
                    #load the same images as selected previously
                    self.display_images()
                    return
            
            #event listner
            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        event.type = pygame.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
            pygame.display.update()

